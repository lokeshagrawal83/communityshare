import logging
import sys

from community_share import config, app

logger = logging.getLogger(__name__)

logger.info('Loading settings from environment')
config.load_from_file()

if not 'production' == config.APP_ENV:
    sys.exit('Cannot run production app without production config')

logger.info('Making application')
app = app.make_app()
app.debug = False
logger.info('Debug={0}'.format(app.debug))
