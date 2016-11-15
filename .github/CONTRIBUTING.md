#
Contributing to CommunityShare

We'd love for you to help improve CommunityShare! Below are some guidelines for
contributing.

Psst: Come to our [meetup](Meetup) every other week! It's a great time to
meet and plan with other CommunityShare contributors.

## Code of Conduct
Please read and follow the Code For America [Code of Conduct](CFACOC).

## Questions?
If you have questions about contributing to CommunityShare, please ask in the
[#communityshare](slack) slack channel. If you aren't on slack, open a github
issue (and if you plan on sticking around, ask to be added to the slack
channel).


## Creating an Issue
Found a problem? Open an issue to let others know and to start collaborating on
a fix! Before you do, search on [GitHub](issues) to check if there is already
an issue open for the problem you found.

Wondering what makes a good issue? Here is a good example:
https://github.com/communityshare/communityshare/issues/108

## Fixing issues
When you find a github issue that you would like to fix, add a comment on the
issue so that others know you are working on it. This helps avoid duplicate
work. If the problem you found doesn't have a github issue _and is small_, just
go ahead and fix it. Otherwise, create an issue so that other contibutors can
see that you are working on that part of the code and can help out if you have
questions.

## Submitting a Pull Request
One way to make changes is to use the edit feature on GitHub. When you
finish editing a file, click on "Commit Changes" to open a new Pull
Request that can be viewed by other contributers. Use the template to
write a helpful summary of your changes, and then submit it! 

Another way to make changes is to use `git` on your local computer. There
are lots of resources online if you want to learn about git; here is
[one](git). As in that guide, you'll want to create a new branch to do
your development on:

```shell
git checkout -b my-fix-branch master
```

Take advantage of the test suite we are building -- run it with `npm
test`. You will also want to test the site itself by starting the server
with `npm start` and trying out the major features to make sure they work
(login, signup, sending messages). Finally, don't forget to use
descriptive commit messages!

Once your changes are on GitHub, send a pull request to
`communityshare:master`. If another contributor asks for changes, please:

* **Make the required updates.**
* **Re-run the test suite and test the site.**
* **Commit your changes to your branch.**
* **Push the changes to your GitHub repository.** This will update your pull
  request. "Ping" the person that requested changes (leaving a github comment
  works well).

See you on Github!

## Style Guide
Use your best judgement when it comes to style decisions.

When you open a pull request, one of our github-integrated tools may point out
some style problems. These tools make mistakes, so feel free to ask about the
messages they generate, but in general, try to fix everything they point out
before accepting changes.

## Credits
This style guide is a heavily modified derivative of AngularJS's [CONTRIBUTING.md](ngContributing)


[ngContributing]:https://github.com/angular/angular.js/blob/master/CONTRIBUTING.md
[CFACOC]:https://github.com/codeforamerica/codeofconduct
[slack]:https://codefortucson.slack.com/messages/communityshare/
[issues]:https://github.com/communityshare/communityshare/issues
[Meetup]:https://www.meetup.com/Code-for-Tucson/
[git]:https://guides.github.com/activities/hello-world/
