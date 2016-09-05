import logging

from community_share import config, setup

logger = logging.getLogger(__name__)

logger.info('Loading settings from environment')
config.load_from_environment()
logger.info('Finished loading settings')
setup(n_random_users=0)
