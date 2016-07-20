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

> Debugging on OS X - use `socat -d -d TCP-L:8099,fork UNIX:/var/run/docker.sock`

After this you should be able to see the servers initialize. You should be able to open up a browser to [http://localhost:5000](http://localhost:5000) and see the CommunityShare site.

If you experience any issues getting CommunityShare running locally, please [file an issue](https://github.com/communityshare/communityshare/issues/new) and describe the problems you encountered.

Should you have need to inspect the running logs, they can be found mounted at `/communitysharelogs` within the Docker container. While the server is running, you can login to the container and explore:

```bash
docker-container exec server sh
```

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
