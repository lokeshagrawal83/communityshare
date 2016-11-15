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

Want to know more or contribute? Check out our [Contribution Guidelines](contrib) and [Developer Guide](developer).

[developer]:https://github.com/communityshare/communityshare/blob/master/developer.md
[contrib]:https://github.com/communityshare/communityshare/blob/master/.github/CONTRIBUTING.md
