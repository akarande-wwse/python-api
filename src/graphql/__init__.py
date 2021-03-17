from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers
from .resolvers import retailer, promo_card

type_defs = load_schema_from_path("src/graphql/schema/")

resolvers = retailer.resolvers

schema = make_executable_schema(
    type_defs, *resolvers, snake_case_fallback_resolvers
)
