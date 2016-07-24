# Community Share

We're working on creating an application to connect educators with community partners.

See [communityshare.us](http://www.communityshare.us) for more details.

[![Slack Status](https://codefortucson-slackin.herokuapp.com/badge.svg)](https://codefortucson.slack.com)
[![CircleCI](https://circleci.com/gh/communityshare/communityshare/tree/master.svg?style=svg)](https://circleci.com/gh/communityshare/communityshare/tree/master)
[![Code Climate](https://codeclimate.com/github/communityshare/communityshare/badges/gpa.svg)](https://codeclimate.com/github/communityshare/communityshare)
[![Issue Count](https://codeclimate.com/github/communityshare/communityshare/badges/issue_count.svg)](https://codeclimate.com/github/communityshare/communityshare)

## Contributing

We currently develop community share locally by means of a Docker image. The image will boot up and load the current app, letting you make code changes without rebuilding the container. **The first step is thus to install [Docker](https://www.docker.com) on your computer**. Please consult the Docker project or guides online for issues installing and running Docker.

### Running a local development environment

Clone the reposity…

```bash
git clone https://github.com/communityshare/communityshare.git
```

…and then start the app.

```bash
cd communityshare

# via docker directly
docker-compose up

# or via npm
npm start
```

After this you should be able to see the servers initialize. You should be able to open up a browser to [http://localhost:5000](http://localhost:5000) and see the CommunityShare site.

If you experience any issues getting CommunityShare running locally, please [file an issue](https://github.com/communityshare/communityshare/issues/new) and describe the problems you encountered.

### Running the test suite

We currently have a working and primitive test suite. It should complete successfully before any PRs are merged.

```bash
# via docker
docker-compose run --rm server python /communityshare/tests.py

# via npm
npm test
```

### Formatting

There is a script to format python files. It should be run before any python PR is merged.

```bash
npm run format
```

By default, this script formats every file in the project, which can take several seconds. You can pass filenames as an additional argument to format only some files, which is much faster.

```bash
npm run format app.py setup.py
```

For Javascript, we have a lint script set up but no automated formatting. The lint script is run just like the format script:

```bash
npm run js-lint [FILE]
```

Please eliminate errors and warnings from any file that you touch in a PR.

### Debugging

Interactive debugging from the commandline using `pdb` is left as an exercise to the reader.
If you want to debug in a more robust IDE, however, that is possible currently with Eclipse (and PyDev) and PyCharm (Professional Edition).

Because of the way the debuggers work, changes to the code will require restarting the server in order to take effect. It can help helpful to start the database and application servers/containers separately so that the database can persist while the app server restarts.

```bash
# Start the database server
docker-compose up -d db

# Start the application server
docker-compose up server
```

The `-d` option tells `docker-compose` to run the database in _daemon_-mode, meaning that it will run in the background and hide the debugging information. Running `server` without the `-d` option runs it in the foreground, shows extra debugging information, and allows you to easily kill the process with `ctrl+c`.

#### Eclipse

You will need to install the [PyDev plugin](https://marketplace.eclipse.org/content/pydev-python-ide-eclipse) for Eclipse and get that setup.
There are helpful tutorials online describing how to get the right debugging views and perspectives setup.

To start debugging, simply start the PyDev server by clicking on its button, then start the application server.

> Note: debugging in Eclipse depends on a custom version of the `pydevd` module, included in this project. The custom changes involve setting up the proper path mapping for the debugger.

#### PyCharm

PyCharm (Professional Edition) supports remote debugging out of the box, but you will need to configure the debugger. Thankfully, you can accomplish this by only setting two fields.

In the debugging tools, select `Edit Configurations` and then add a new `Python remote debug`.

![Remote debugging settings](/docs/images/pycharm-remote-debug-settings.png)

 - `hostname = 0.0.0.0`
# via docker
 - `post = 5678`

To start debugging, start the remote debugging tool and start the application server. When PyCharm loads the initial breakpoint, it will ask to specify the path mapping. It is sufficient to let it automatically detect the path mapping.
npm test
```

#### Other Debugging

There is a script to format python files. It should be run before any python PR is merged.

```bash
npm run format
```

### Docker Notes

#### PyCharm and Docker

PyCharm has built-in support for many Docker operations and debugging. However, its support was built upon `docker-machine` and friends, which are not the recommended or supported way of running Docker in this project. In order to use the native Docker implementation on OS X, PyCharm needs to be tricked into connecting to a fake `docker-machine` instance.

You can connect a `Docker Deployment` under `Edit Configurations` with the following settings.

![Docker Deployment Settings](/docs/images/pycharm-docker-deployment-settings.png)

 - `API URL = tcp://localhost:8099`
 - `Certificates folder = ~/.docker/machine/certs`

Additionally, in order to "trick" PyCharm, you will need to use something like `socat` to translate between the local socket and the TCP connection.

```bash
socat -d -d TCP-L:8099,fork UNIX:/var/run/docker.sock
```
