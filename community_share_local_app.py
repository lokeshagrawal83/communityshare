import logging
import sys

from community_share import config, app

logger = logging.getLogger(__name__)

logger.info('Loading settings from environment')
config.load_config('./config.dev.json')

if 'production' == config.APP_ENV:
    sys.exit('Cannot run development app with production config')

logger.info('Making application')
app = app.make_app()
app.debug = True
logger.info('Debug={0}'.format(app.debug))
app.run(host='0.0.0.0', port=5000, extra_files=['./manifest.json'])
