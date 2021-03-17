from sqlalchemy import BigInteger, CHAR, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Table, Text, UniqueConstraint, text, and_
from sqlalchemy.orm import relationship, defer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Card(Base):
    __tablename__ = 'card'

    cardid = Column(Integer, primary_key=True)
    carddesc = Column(Text)
    cardimagename = Column(Text)
    carddisplayorder = Column(Integer)
    cardtemplate = Column(Text)

    category = relationship('Category', secondary='catcardmap')


class CardRecipientInfo(Base):
    __tablename__ = 'cardrecipientinfo'

    carddetid = Column(ForeignKey('carddet.carddetid'), primary_key=True, nullable=False)
    recipientname   = Column(Text, nullable=False)
    recipientemail  = Column(Text, nullable=False)


class CardSenderInfo(Base):
    __tablename__ = 'cardsenderinfo'

    carddetid = Column(ForeignKey('carddet.carddetid'), primary_key=True, nullable=False)
    sendername = Column(Text, nullable=False)
    senderemail = Column(Text, nullable=False)


class CardTextDetail(Base):
    __tablename__ = 'cardtextdetail'
    __table_args__ = (
        UniqueConstraint('retailerid', 'clientid', 'cardid', 'ctdtext'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('cardtextdetail_id_seq'::regclass)"))
    retailerid = Column(Integer, nullable=False)
    clientid = Column(Integer, nullable=False, server_default=text("'-1'::integer"))
    cardid = Column(Integer, nullable=False)
    ctdtext = Column(Text, nullable=False)
    ctdstyle = Column(Text, nullable=False)


class Category(Base):
    __tablename__ = 'category'

    catid = Column(Integer, primary_key=True, server_default=text("nextval('category_catid_seq'::regclass)"))
    catdesc = Column(Text)
    catdisplayorder = Column(Integer)

    cards = relationship('Card', secondary='catcardmap', lazy='joined')


class Client(Base):
    __tablename__ = 'client'
    __table_args__ = (
        CheckConstraint("(active)::text = ANY (ARRAY[('Y'::character varying)::text, ('N'::character varying)::text])"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(String(1), nullable=False, server_default=text("'Y'::character varying"))


class Retailer(Base):
    __tablename__ = 'retailer'

    retailerid = Column(Integer, primary_key=True)
    retailername = Column(Text, nullable=False)
    retaileractive = Column(CHAR(1), nullable=False, server_default=text("'Y'::bpchar"))
    groupid = Column(Text, nullable=False)
    merchantid = Column(Text)

    categories = relationship('Category', secondary='retailercategorymap')
    retailer_profiles = relationship('RetailerProfile')


class RetailerCardNumber(Base):
    __tablename__ = 'retailercardnumbers'
    __table_args__ = (
        UniqueConstraint('giftcardnumber', 'serialnumber', 'retailerid'),
    ) 

    retailerid = Column(ForeignKey('retailer.retailerid'), nullable=False)
    status = Column(Text)
    receivedate = Column(BigInteger)
    giftcardnumber = Column(Text)
    serialnumber = Column(Text)
    amount = Column(Float(53))
    expirationdate = Column(BigInteger)
    cleansedgcnumber = Column(Text)
    carddetid = Column(ForeignKey('carddet.carddetid'), index=True) # manually changed
    rcnid = Column(BigInteger, primary_key=True, server_default=text("nextval('retailercardnumbers_rcnid_seq'::regclass)"))

    retailer = relationship('Retailer', lazy=False)


class RetailerProfile(Base):
    __tablename__ = 'retailerprofile'

    retailerid = Column(ForeignKey('retailer.retailerid'), primary_key=True, nullable=False)
    retailerprofilename = Column(Text, primary_key=True, nullable=False)
    retailerprofilevalue = Column(Text)


class CardDetail(Base):
    __tablename__ = 'carddet'

    carddetid = Column(BigInteger, primary_key=True, server_default=text("nextval('carddet_carddetid_seq'::regclass)"))
    cardid = Column(Integer) 
    transid = Column(Integer, index=True)
    retailerid = Column(ForeignKey('retailer.retailerid'), index=True)
    lineitemid = Column(Integer)
    denomination = Column(Float(53))
    personalmessage = Column(Text)
    cdstatus = Column(CHAR(1), nullable=False, index=True, server_default=text("'H'::bpchar"))
    createdate = Column(DateTime, nullable=False, server_default=text("now()"))
    cardimage = Column(Text)
    clientid = Column(Integer, nullable=False, server_default=text("1"))
    clientcardsrno = Column(String(50), index=True)
    errorretry = Column(Integer, nullable=False, server_default=text("0"))
    merchantid = Column(Text)
    reissuecarddetid = Column(BigInteger)
    shipdatetime = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    retailer = relationship('Retailer')
    invoice = relationship('Invoice', secondary='invlineitems')
    cardsenderinfo = relationship('CardSenderInfo', lazy='joined', innerjoin=True, uselist=False) # manually added
    cardrecipientinfo = relationship('CardRecipientInfo', lazy='joined', innerjoin=True, uselist=False) # manually added
    retailercardnumbers = relationship(
        'RetailerCardNumber',
        primaryjoin=and_(RetailerCardNumber.carddetid == carddetid, RetailerCardNumber.status == 'A')
    ) # manually added
    card = relationship('Card', primaryjoin='foreign(CardDetail.cardid) == remote(Card.cardid)')
    reissuecarddet = relationship('CardDetail', primaryjoin='foreign(CardDetail.reissuecarddetid) == remote(CardDetail.carddetid)')


t_catcardmap = Table(
    'catcardmap', metadata,
    Column('catid', ForeignKey('category.catid'), nullable=False),
    Column('cardid', ForeignKey('card.cardid'), nullable=False)
)

t_retailercategorymap = Table(
    'retailercategorymap', metadata,
    Column('catid', ForeignKey('category.catid'), nullable=False),
    Column('retailerid', ForeignKey('retailer.retailerid'), nullable=False),
    UniqueConstraint('catid', 'retailerid')
)


class UserTrans(Base):
    __tablename__ = 'usertrans'

    usertransid = Column(BigInteger, primary_key=True, server_default=text("nextval('usertrans_usertransid_seq'::regclass)"))
    utdate = Column(BigInteger)
    utipaddr = Column(Text)
    retailerid = Column(ForeignKey('retailer.retailerid'), nullable=False)
    utrefererurl = Column(Text)
    merchantid = Column(Text)

    retailer = relationship('Retailer')


t_invlineitems = Table(
    'invlineitems', metadata,
    Column('invno', ForeignKey('invoice.invno'), primary_key=True, nullable=False),
    Column('carddetid', ForeignKey('carddet.carddetid'), primary_key=True, nullable=False)
)

class Invoice(Base):
    __tablename__ = 'invoice'

    invno = Column(BigInteger, primary_key=True, server_default=text("nextval('invoice_invno_seq'::regclass)"))
    invtransid = Column(ForeignKey('usertrans.usertransid'), nullable=False, index=True)
    invdate = Column(BigInteger, nullable=False, index=True)
    invtotal = Column(Float(53))
    invstatus = Column(Text, index=True)
    invordernum = Column(Text, index=True)
    clientordersrno = Column(Text, unique=True)
    groupid = Column(Text)
    merchantid = Column(Text)
    merchantname = Column(Text)
    retailername = Column(Text)
    retailerlogo = Column(Text)

    invlineitems = relationship(
        'CardDetail', 
        secondary='invlineitems',
        secondaryjoin=and_(t_invlineitems.c.carddetid == CardDetail.carddetid, CardDetail.cdstatus != 'X')
    ) # manually added
    usertran = relationship('UserTrans')
    invpaymentdetails = relationship('InvPaymentDetail', innerjoin=True)


class InvPaymentDetail(Base):
    __tablename__ = 'invpaymentdetails'

    ipdsrno = Column(BigInteger, primary_key=True, server_default=text("nextval('invpaymentdetails_ipdsrno_seq'::regclass)"))
    ipdinvno = Column(ForeignKey('invoice.invno'), nullable=False, index=True)
    ipdpcamt = Column(Float(53))
    ipdpaymentstatus = Column(Text)
    ipdpcfname = Column(Text)
    ipdpclname = Column(Text)
    ipdemailid = Column(Text, index=True)
    ipdpcresponsemsg = Column(Text)
    ipdpcnoquad = Column(Text)
    ipdsettlementdate = Column(DateTime, nullable=False, server_default=text("now()"))
    ipdpcauthreceiptno = Column(Text)
    ipdcctype = Column(Text)
    ipdinvpaymenttoken = Column(Text)

    invoice = relationship('Invoice')


class CustomStyle(Base):
    __tablename__ = 'customstyle'

    styleid = Column(Integer, primary_key=True)
    groupid = Column(Text, nullable=False)
    merchantid = Column(Text)
    active = Column(Text)
    

class PromoConfig(Base):
    __tablename__ = 'promoconfig'
    
    pcid = Column(Integer, primary_key=True, server_default=text("nextval('promoconfig_pcid_seq'::regclass)"))
    groupid = Column(Text, nullable=False)
    merchantid = Column(Text)
    fromdate = Column(DateTime)
    todate = Column(DateTime)
    catid = Column(Integer)
    bannername = Column(Text)
    
    
class PromoConfigDetail(Base):
    __tablename__ = 'promoconfigdtl'
    
    pcdid = Column(Integer, primary_key=True, server_default=text("nextval('promoconfigdtl_pcdid_seq'::regclass)"))
    pcid = Column(ForeignKey('promoconfig.pcid'), nullable=False, index=True)
    qty = Column(Integer, server_default=text("1"))
    minvalue = Column(Float(17))
    dollarvalue = Column(Float(17))