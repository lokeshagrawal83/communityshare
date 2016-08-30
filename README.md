# Community Share

We're working on creating an application to connect educators with community partners.

See [communityshare.us](http://www.communityshare.us) for more details.


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