import graphene
import graphql_jwt
import core.schema

class Query(core.schema.Query, graphene.ObjectType):
    # This is a test field to prove we are using the right file
    debug_check = graphene.String()
    
    def resolve_debug_check(root, info):
        return "I am working!"

class Mutation(core.schema.Mutation, graphene.ObjectType):
    # We are forcing the Auth logic here
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)