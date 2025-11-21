import base64
from django.core.files.base import ContentFile
import graphql_jwt
import graphene
from graphene_django import DjangoObjectType
from django.db import models
from .models import User, Post, Comment, Like, Follow, Share, Notification, Message

# TYPES

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar", "is_verified")

    followers_count = graphene.Int()
    following_count = graphene.Int()
    is_following = graphene.Boolean()
    
    post_set = graphene.List(lambda: PostType)

    def resolve_followers_count(self, info):
        return Follow.objects.filter(following=self).count()

    def resolve_following_count(self, info):
        return Follow.objects.filter(follower=self).count()

    def resolve_is_following(self, info):
        user = info.context.user
        if user.is_anonymous: return False
        return Follow.objects.filter(follower=user, following=self).exists()
    
    def resolve_post_set(self, info):
        return Post.objects.filter(author=self).order_by('-created_at')

class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ("id", "user", "post")

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "author", "post", "text", "created_at")

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "author", "content", "image", "created_at", "likes", "comments")

class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "created_at")

class ShareType(DjangoObjectType):
    class Meta:
        model = Share
        fields = ("id", "original_post", "shared_by", "message", "created_at")

class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = ("id", "recipient", "sender", "notification_type", "post", "is_read", "created_at")

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ("id", "sender", "receiver", "content", "is_read", "created_at")        


# QUERIES

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    my_notifications = graphene.List(NotificationType)
    get_messages = graphene.List(MessageType, friend_id=graphene.ID(required=True))
    
    user = graphene.Field(UserType, id=graphene.ID(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_my_notifications(root, info):
        user = info.context.user
        if user.is_anonymous: return []
        return Notification.objects.filter(recipient=user).order_by('-created_at')

    def resolve_get_messages(root, info, friend_id):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        friend = User.objects.get(id=friend_id)
        return Message.objects.filter(
            (models.Q(sender=user) & models.Q(receiver=friend)) |
            (models.Q(sender=friend) & models.Q(receiver=user))
        ).order_by('created_at')

    def resolve_user(root, info, id):
        return User.objects.get(pk=id)    


# MUTATIONS

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    class Arguments:
        content = graphene.String(required=True)
        image_data = graphene.String(required=False) 

    def mutate(self, info, content, image_data=None):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        post = Post(content=content, author=user)

        if image_data:
            try:
                format, imgstr = image_data.split(';base64,') 
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f"post_image.{ext}")
                post.image = data
            except Exception as e:
                print("Image decode error:", e)
        
        post.save()
        return CreatePost(post=post)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    class Arguments:
        post_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, post_id, text):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        post = Post.objects.get(id=post_id)
        comment = Comment(author=user, post=post, text=text)
        comment.save()
        if post.author != user:
            Notification.objects.create(recipient=post.author, sender=user, notification_type='comment', post=post)
        return CreateComment(comment=comment)


class LikePost(graphene.Mutation):
    user = graphene.Field(UserType)
    post = graphene.Field(PostType)
    class Arguments:
        post_id = graphene.ID(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        post = Post.objects.get(id=post_id)
        existing_like = Like.objects.filter(user=user, post=post)
        if existing_like.count() > 0:
            existing_like.delete()
        else:
            Like.objects.create(user=user, post=post)
            if post.author != user:
                Notification.objects.create(recipient=post.author, sender=user, notification_type='like', post=post)
        return LikePost(user=user, post=post)


class FollowUser(graphene.Mutation):
    ok = graphene.Boolean()
    class Arguments:
        user_id = graphene.ID(required=True)

    def mutate(self, info, user_id):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        target_user = User.objects.get(id=user_id)
        if user == target_user: raise Exception("Cannot follow self")
        
        existing_follow = Follow.objects.filter(follower=user, following=target_user)
        if existing_follow.count() > 0:
            existing_follow.delete()
            return FollowUser(ok=False) 
        else:
            Follow.objects.create(follower=user, following=target_user)
            Notification.objects.create(recipient=target_user, sender=user, notification_type='follow', post=None)
            return FollowUser(ok=True)


class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return RegisterUser(user=user)


class SharePost(graphene.Mutation):
    share = graphene.Field(ShareType)
    class Arguments:
        post_id = graphene.ID(required=True)
        message = graphene.String(required=False)

    def mutate(self, info, post_id, message=None):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        post = Post.objects.get(id=post_id)
        share = Share(original_post=post, shared_by=user, message=message)
        share.save()
        return SharePost(share=share)


class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)
    class Arguments:
        receiver_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, receiver_id, content):
        user = info.context.user
        if user.is_anonymous: raise Exception("Not logged in!")
        receiver = User.objects.get(id=receiver_id)
        msg = Message(sender=user, receiver=receiver, content=content)
        msg.save()
        return SendMessage(message=msg)        


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    like_post = LikePost.Field()
    follow_user = FollowUser.Field()
    register_user = RegisterUser.Field()
    share_post = SharePost.Field()
    send_message = SendMessage.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)    