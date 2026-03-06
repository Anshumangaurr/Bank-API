import graphene
from models import session, Branch, Bank


class BankType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()


class BranchType(graphene.ObjectType):
    id = graphene.Int()
    branch = graphene.String()
    ifsc = graphene.String()
    address = graphene.String()
    bank = graphene.Field(BankType)


# manual connection so GraphQL produces edges/nodes structure for pagination
class BranchConnection(graphene.Connection):
    class Meta:
        node = BranchType


class Query(graphene.ObjectType):
    branches = graphene.ConnectionField(BranchConnection)

    def resolve_branches(root, info, **kwargs):
        # ignore pagination args for simplicity; Graphene will slice results
        return session.query(Branch).all()


schema = graphene.Schema(query=Query)