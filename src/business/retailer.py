from ..database.models import Retailer as RetailerModel, RetailerProfile, UserTrans, CustomStyle, Category, Card
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from ..utils import response
import requests, time, json
from ..config import EGC_SPOTON_GROUP_API, EGC_PAYMENT_TOKEN_KEY_API, EGC_DEFAULT_GROUPID

class Retailer:
    def __init__(self, context):
        self.session = context["session"]
        self.referer = context["referer"]

    def __args(self, *keys):
        return [self.args[key] for key in keys]


    def __retailer(self, groupid: str, merchantid: str):
        try:
            retailer = self.session.query(RetailerModel).filter(
                and_(RetailerModel.groupid == groupid, RetailerModel.merchantid == merchantid)
            ).one()
            return retailer
        except NoResultFound:
            return None


    def __find_retailer(self, groupid: str, merchantid: str):
        retailer = self.__retailer(groupid, merchantid)
        if not retailer:
            retailer = self.__retailer(groupid, None)
        if not retailer:
            retailer = self.__retailer(EGC_DEFAULT_GROUPID, None)
        return retailer


    def __custom_style(self, groupid: str, merchantid: str):
        custom_style = self.session.query(CustomStyle).filter(
            and_(CustomStyle.groupid == groupid, CustomStyle.merchantid == merchantid)
        ).first()
        return custom_style


    def __find_custom_style(self, groupid: str, merchantid: str):
        custom_style = self.__custom_style(groupid, merchantid)
        if not custom_style:
            custom_style = self.__custom_style(groupid, None)
        if not custom_style:
            custom_style = self.__custom_style(EGC_DEFAULT_GROUPID, None)
        return custom_style


    def __create_user_trans(self, retailer, merchantid: str):
        merchant = {
            "groupId": retailer.groupid,
            "merchantId": merchantid,
            "retailerName": retailer.retailername,
            "retailerLogo": retailer.retailer_logo,
        }
        user_trans = UserTrans(
            utdate=round(time.time() * 1000),
            utipaddr="",
            retailerid=retailer.retailerid,
            utrefererurl=self.referer or "",
            merchantid=json.dumps(merchant),
        )
        try:
            self.session.add(user_trans)
            self.session.commit()
            return user_trans.usertransid
        except Exception:
            self.session.rollback()
            raise


    def get_retailer(self, groupid: str, merchantid: str):
        try:
            # find retailer by merchantid or groupid
            retailer = self.__find_retailer(groupid, merchantid)
            retailer.merchant_id = merchantid
            # get merchant data from spoton api
            merchant_data = requests.get(EGC_SPOTON_GROUP_API + f"?merchantId={merchantid}").json()
            retailer.retailer_logo = merchant_data["logoUrl"]
            # add entry in usertrans table
            retailer.trans_id = self.__create_user_trans(retailer, merchantid)
            # get token key from payment api
            token_key = requests.get(EGC_PAYMENT_TOKEN_KEY_API + merchantid + f"?json_only").json()
            retailer.token_key = token_key["nmi_tokenization_key"]
            # find style info by merchantid or groupid
            retailer.custom_style = self.__find_custom_style(groupid, merchantid)
            return response(retailer, True, "Success")
        except Exception as error:
            print(f"Error inside find_retailer: {error}")
            return response(RetailerModel(), False, "Failed to fetch retailer")
