from ..database.models import PromoConfig, PromoConfigDetail
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from ..utils import response
import time

class PromoCard:
    def __init__(self, context):
        self.session = context["session"]
        
    def getPromoCard(args):
        pass