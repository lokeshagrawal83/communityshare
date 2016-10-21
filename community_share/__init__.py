import os
import logging
import sys

from functools import wraps
from typing import Any, Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from community_share.config import load_app_config
from community_share.crypt import CryptHelper

Base = declarative_base()

logger = logging.getLogger(__name__)


def create_file_logger(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return logging.FileHandler(path)


def create_stdout_logger():
    return logging.StreamHandler(stream=sys.stdout)


def setup_logging(level, directory):

    if directory == 'STDOUT':
        handler = create_stdout_logger()
    else:
        handler = create_file_logger(os.path.join(directory, 'community_share.log'))

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    for package in {'__main__', 'community_share'}:
        module_logger = logging.getLogger(package)
        module_logger.addHandler(handler)
        module_logger.setLevel(level)


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


def with_store(f: Callable[..., Any]) -> Callable[..., Any]:
    """Provides the SqlAlchemy store to a function

    Use this instead of importing `communityshare.store`
    directly in order to make testing easy

    **Example**
    This creates a new in-memory store for testing

    .. sourcecode Python

       class Store():
          engine = create_engine('sqlite:///:memory:')
          Session = sessionmaker(bind=engine)
          session = Session()

       normally_wrapped_function(store=Store())

    :param f: function to wrap
    :return: new function with `store` param injected
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        actual_store = kwargs.pop('store', store)
        return f(*args, store=actual_store, **kwargs)

    return wrapped


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
