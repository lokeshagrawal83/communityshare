import os
import logging
import json
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from community_share.crypt import CryptHelper

Base = declarative_base()

logger = logging.getLogger(__name__)

def setup_logging(level, location):
    "Utility function for setting up logging."
    if not os.path.exists(location):
        os.makedirs(location)
    logging_fn = os.path.join(location, 'community_share.log')
    if not os.path.exists(logging_fn):
        open(logging_fn, 'a').close()
    ch = logging.FileHandler(logging_fn)
    if location == "STDOUT":
        ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    # Which packages do we want to log from.
    packages = ('__main__', 'community_share',)
    for package in packages:
        logger = logging.getLogger(package)
        logger.handlers = []
        logger.addHandler(ch)
        logger.setLevel(level)
    # Warning only packages
    packages = []
    for package in packages:
        logger = logging.getLogger(package)
        logger.addHandler(ch)
        logger.setLevel(logging.WARNING)
    logger.debug('Finished setting up logging.')
    
class Store(object):

    def __init__(self):
        pass

    def set_config(self, config):
        logger.info('Creating database engine with {0}'.format(config.DB_CONNECTION))
        self._engine = create_engine(config.DB_CONNECTION)
        self._session = scoped_session(sessionmaker(bind=self._engine))

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

store = Store()


class Config(object):
    NAMES = (
        # Database
        'DB_CONNECTION',
        # Email 
        'MAILER_TYPE', # Can be 'MAILGUN' or 'DUMMY' or 'QUEUE'
        'MAILGUN_API_KEY', 'MAILGUN_DOMAIN', 'DONOTREPLY_EMAIL_ADDRESS', 'SUPPORT_EMAIL_ADDRESS',
        'BUG_EMAIL_ADDRESS', 'ABUSE_EMAIL_ADDRESS', 'ADMIN_EMAIL_ADDRESSES', 'NOTIFY_EMAIL_ADDRESS',
        # Location
        'BASEURL',
        # Logging
        'LOGGING_LEVEL', 'LOGGING_LOCATION',
        # S3 bucket
        'S3_BUCKETNAME', 'S3_KEY', 'S3_USERNAME', 'UPLOAD_LOCATION',
        # Version
        'COMMIT_HASH',
        # Cryptography
        'ENCRYPTION_KEY',
        # SSL
        'SSL',
    )
    def load_from_dict(self, d):
        if set(d.keys()) != set(self.NAMES):
            error = 'Missing keys are {0} and extra keys are {1}'.format(
                set(self.NAMES) - set(d.keys()),
                set(d.keys()) - set(self.NAMES))
            raise ValueError("Bad config. : " + error)
        for key, value in d.items():
            setattr(self, key, value)
        setup_logging(self.LOGGING_LEVEL, self.LOGGING_LOCATION)
        logger.info('Setup logging with level {0}'.format(self.LOGGING_LEVEL))
        store.set_config(self)
        self.crypt_helper = CryptHelper(config.ENCRYPTION_KEY)

    def load_from_environment(self):
        data = {
            'DB_CONNECTION': os.environ['DATABASE_URL'],
            'MAILER_TYPE': os.environ['COMMUNITYSHARE_MAILER_TYPE'],
            'MAILGUN_API_KEY': os.environ['MAILGUN_API_KEY'],
            'MAILGUN_DOMAIN': os.environ['MAILGUN_DOMAIN'],
            'LOGGING_LEVEL': os.environ['COMMUNITYSHARE_LOGGING_LEVEL'],
            'DONOTREPLY_EMAIL_ADDRESS': os.environ['COMMUNITYSHARE_DONOTREPLY_EMAIL_ADDRESS'],
            'SUPPORT_EMAIL_ADDRESS': os.environ['COMMUNITYSHARE_SUPPORT_EMAIL_ADDRESS'],
            'BUG_EMAIL_ADDRESS': os.environ['COMMUNITYSHARE_BUG_EMAIL_ADDRESS'],
            'ABUSE_EMAIL_ADDRESS': os.environ['COMMUNITYSHARE_ABUSE_EMAIL_ADDRESS'],
            'ADMIN_EMAIL_ADDRESSES': os.environ['COMMUNITYSHARE_ADMIN_EMAIL_ADDRESSES'],
            'NOTIFY_EMAIL_ADDRESS': os.environ['COMMUNITYSHARE_NOTIFY_EMAIL_ADDRESS'],
            'BASEURL': os.environ['COMMUNITYSHARE_BASEURL'],
            'S3_BUCKETNAME': os.environ['COMMUNITYSHARE_S3_BUCKETNAME'],
            'S3_KEY': os.environ['COMMUNITYSHARE_S3_KEY'],
            'S3_USERNAME': os.environ['COMMUNITYSHARE_S3_USERNAME'],
            'UPLOAD_LOCATION': os.environ['COMMUNITYSHARE_UPLOAD_LOCATION'],
            'COMMIT_HASH': os.environ['COMMIT_HASH'],
            'ENCRYPTION_KEY': os.environ['COMMUNITYSHARE_ENCRYPTION_KEY'],
            'SSL': os.environ.get('COMMUNITYSHARE_SSL', 'FORCE_SSL'),
        }
        self.load_from_dict(data)

    def config_filename(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        fn = os.path.join(directory, '..', 'config.json')
        return fn
        
    def load_from_file(self):
        fn = self.config_filename()
        with open(fn, 'r') as f:
            config_data = json.load(f)
            self.load_from_dict(config_data)

    def write_file(self):
        d = {}
        for name in self.NAMES:
            d[name] = getattr(self, name)
        fn = self.config_filename()
        with open(fn, 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4, separators=(',', ': '))
            

config = Config()
