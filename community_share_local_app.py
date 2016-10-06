import logging
import os.path
import sys
import time

from community_share import config, app
import setup_test


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

logger.info('Loading settings from environment')
config.load_config('./config.dev.json')

if 'production' == config.APP_ENV:
    sys.exit('Cannot run development app with production config')

setup_test.setup(n_random_users=40)

wait_for_manifest(config.WEBPACK_MANIFEST_PATH)

logger.info('Making application')
app = app.make_app()
app.debug = True
logger.info('Debug={0}'.format(app.debug))
app.run(host='0.0.0.0', port=5000, extra_files=['./manifest.json'])
