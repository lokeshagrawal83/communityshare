import logging
import os
import sys
import time

from community_share import config, app
from debugger import can_connect_to_debugger, inject_debugger


def wait_for_manifest(path):
    print('waiting for webpack manifest... {}'.format(path))

    if not os.path.exists(path):
        print(
            'Waiting for webpack to create manifest.json\n'
            'Please ensure that the webpack process is running\n'
            'or has run already. `docker-compose up webpack`'
        )

    while not os.path.exists(path):
        print('\tstill not found, trying again in five seconds...')
        time.sleep(5)


logger = logging.getLogger(__name__)

if can_connect_to_debugger():
    logger.info('Connecting to debugger')
    inject_debugger()
else:
    logger.info('Could not find any debugger')

logger.info('Loading settings from environment')
config.load_config('./config.dev.json')

if 'production' == config.APP_ENV:
    sys.exit('Cannot run development app with production config')

wait_for_manifest(config.WEBPACK_MANIFEST_PATH)

logger.info('Making application')
app = app.make_app()
app.debug = True
logger.info('Debug={0}'.format(app.debug))
app.run(
    host='0.0.0.0',
    port=5000,
    debug=True,
    use_debugger=False,
    use_reloader=False,
    extra_files=['./manifest.json']
)
