
def map_resolver(obj, resolver):
    for key, value in resolver.items():
        obj.field(key)(value)


def response(obj, status, message):
    obj.status = status
    obj.message = message
    return obj