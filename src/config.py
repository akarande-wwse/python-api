"""App configuration."""
from os import environ, path
from dotenv import load_dotenv

# Find .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# General Config
EGC_WEB_BUILD_DIR       =   environ.get('EGC_WEB_BUILD_DIR')
EGC_ASSET_BASE_PATH     =   environ.get('EGC_ASSET_BASE_PATH')
EGC_SECRET              =   environ.get('EGC_SECRET')
EGC_GOOGLE_TRACKING_ID  =   environ.get('EGC_GOOGLE_TRACKING_ID')
EGC_CARD_SECRET         =   environ.get('EGC_CARD_SECRET')

# Database config
EGC_DB_HOSTNAME         =   environ.get('EGC_DB_HOSTNAME')
EGC_DB_PORT             =   environ.get('EGC_DB_PORT')
EGC_DB_NAME             =   environ.get('EGC_DB_NAME')
EGC_DB_USERNAME         =   environ.get('EGC_DB_USERNAME')
EGC_DB_PASSWORD         =   environ.get('EGC_DB_PASSWORD')
EGC_DATABASE_URI        =   'postgresql://{username}:{password}@{hostname}:{db_port}/{db_name}'.format(
                                username=EGC_DB_USERNAME,
                                password=EGC_DB_PASSWORD,
                                hostname=EGC_DB_HOSTNAME,
                                db_port=EGC_DB_PORT,
                                db_name=EGC_DB_NAME
                            )

EGC_SPOTON_GROUP_API        =   environ.get('EGC_SPOTON_GROUP_API')
EGC_PAYMENT_TOKEN_KEY_API   =   environ.get('EGC_PAYMENT_TOKEN_KEY_API')

EGC_DEFAULT_GROUPID     =   '1001'
