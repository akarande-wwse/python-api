from ariadne import ObjectType
from ...business.promo_card import PromoCard
from ...utils import map_resolver

query = ObjectType("Query")
promo_card = ObjectType("PromoCard")

@query.field("getPromoCard")
def getPromoCard(_, info, **args):
    print(f"Input args: {args}")
    promo = PromoCard(info.context)
    return promo.getPromoCard(args)
    
map_resolver(promo_card, {
    "promoAmount": lambda obj: obj.dollarValue,
    "quantity": lambda obj: obj.qty
})

resolvers = (query, promo_card)