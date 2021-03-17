from ariadne import ObjectType
from ...business.retailer import Retailer
from ...utils import map_resolver

query = ObjectType("Query")
retailer = ObjectType("Retailer")

@query.field("getRetailer")
def get_retailer(_, info, **args):
    print(f"Input args: {args}")
    ret = Retailer(info.context)
    return ret.get_retailer(**args)


def resolve_custom_style(obj, *_):
    custom_style = obj.custom_style
    if custom_style:
        groupid = custom_style.groupid
        merchantid = custom_style.merchantid
        if merchantid:
            return f"merchant/{merchantid}/style.css"
        return f"group/{groupid}/style.css"
    return None

map_resolver(retailer, {
    "retailerId": lambda obj, *_: obj.retailerid,
    "groupId": lambda obj, *_: obj.groupid,
    "retailerName": lambda obj, *_: obj.retailername,
    "retailerActive": lambda obj, *_: obj.retaileractive,
    "bannerName": lambda obj, *_: "",
    "customStyle": resolve_custom_style,
})

resolvers = query, retailer
