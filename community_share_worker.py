#! /usr/bin/python3

import os
import logging
import argparse

from community_share import worker, config

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_pid_dir = os.path.join('var', 'run', 'cs_worker')
    parser.add_argument('--pid-dir', dest='pid_dir', default=default_pid_dir)
    args = parser.parse_args()
    if args.pid_dir is not None:
        pid = str(os.getpid())
        with open(os.path.join(args.pid_dir, 'cs_worker.pid'), 'w') as f:
            f.write(pid)
    config.load_config('./config.production.json')
    logger.info('Starting community share worker.')
    worker.work_loop()
