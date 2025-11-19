import graphene
from graphene_django import DjangoObjectType
from django.db import models
from .models import User, Post, Comment, Like, Follow, Share, Notification, Message

# TYPES

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar", "is_verified")

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

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_my_notifications(root, info):
        user = info.context.user
        if user.is_anonymous:
            return []
        # Return newest notifications first
        return Notification.objects.filter(recipient=user).order_by('-created_at')

    def resolve_get_messages(root, info, friend_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
            
        friend = User.objects.get(id=friend_id)
        
        # Get messages where (Sender is Me AND Receiver is Friend) OR (Sender is Friend AND Receiver is Me)
        return Message.objects.filter(
            (models.Q(sender=user) & models.Q(receiver=friend)) |
            (models.Q(sender=friend) & models.Q(receiver=user))
        ).order_by('created_at')    


# MUTATIONS

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)

    def mutate(self, info, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        
        post = Post(content=content, author=user)
        post.save()
        
        return CreatePost(post=post)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, post_id, text):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        
        post = Post.objects.get(id=post_id)
        
        comment = Comment(author=user, post=post, text=text)
        comment.save()

        # NOTIFICATION TRIGGER
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                sender=user,
                notification_type='comment',
                post=post
            )
        
        return CreateComment(comment=comment)


class LikePost(graphene.Mutation):
    user = graphene.Field(UserType)
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.ID(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")

        post = Post.objects.get(id=post_id)

        existing_like = Like.objects.filter(user=user, post=post)

        if existing_like.count() > 0:
            # Unlike: Delete the like
            existing_like.delete()
        else:
            # Like: Create the like
            Like.objects.create(user=user, post=post)

            # NOTIFICATION TRIGGER
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=user,
                    notification_type='like',
                    post=post
                )

        return LikePost(user=user, post=post)


class FollowUser(graphene.Mutation):
    ok = graphene.Boolean()
    
    class Arguments:
        user_id = graphene.ID(required=True)

    def mutate(self, info, user_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")

        target_user = User.objects.get(id=user_id)
        
        if user == target_user:
             raise Exception("You cannot follow yourself.")

        existing_follow = Follow.objects.filter(follower=user, following=target_user)

        if existing_follow.count() > 0:
            # Unfollow
            existing_follow.delete()
            return FollowUser(ok=False) 
        else:
            # Follow
            Follow.objects.create(follower=user, following=target_user)

            # NOTIFICATION TRIGGER
            Notification.objects.create(
                recipient=target_user,
                sender=user,
                notification_type='follow',
                post=None # Follows don't link to a specific post
            )

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
        if user.is_anonymous:
            raise Exception("Not logged in!")

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
        if user.is_anonymous:
            raise Exception("Not logged in!")

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