import os
import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from community_share.config import load_app_config
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
    packages = ('__main__', 'community_share')
    for package in packages:
        logger = logging.getLogger(package)
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
    NAMES = {
        'APP_ENV',  # 'development' or 'production'
        # Database
        'DB_CONNECTION',
        # Email 
        'MAILER_TYPE',  # Can be 'MAILGUN' or 'DUMMY' or 'QUEUE'
        'MAILGUN_API_KEY',
        'MAILGUN_DOMAIN',
        'DONOTREPLY_EMAIL_ADDRESS',
        'SUPPORT_EMAIL_ADDRESS',
        'BUG_EMAIL_ADDRESS',
        'ABUSE_EMAIL_ADDRESS',
        'ADMIN_EMAIL_ADDRESSES',
        'NOTIFY_EMAIL_ADDRESS',
        # Location
        'BASEURL',
        # Logging
        'LOGGING_LEVEL',
        'LOGGING_LOCATION',
        # S3 bucket
        'S3_BUCKETNAME',
        'S3_KEY',
        'S3_USERNAME',
        'UPLOAD_LOCATION',
        # Cryptography
        'ENCRYPTION_KEY',
        # SSL
        'SSL',
        'WEBPACK_ASSETS_URL',
        'WEBPACK_MANIFEST_PATH',
    }

    def load_config(self, filename):
        data = load_app_config(self.NAMES, filename)

        if set(data.keys()) != self.NAMES:
            missing_keys = self.NAMES - set(data.keys())
            invalid_keys = set(data.keys()) - self.NAMES

            sys.exit(
                'Invalid configuration found:\n\tmissing keys: {}\n\tinvalid keys: {}'
                .format(missing_keys, invalid_keys)
            )

        for key, value in data.items():
            setattr(self, key, value)

        setup_logging(self.LOGGING_LEVEL, self.LOGGING_LOCATION)
        logger.info('Setup logging with level {0}'.format(self.LOGGING_LEVEL))
        store.set_config(self)
        self.crypt_helper = CryptHelper(config.ENCRYPTION_KEY)


config = Config()
