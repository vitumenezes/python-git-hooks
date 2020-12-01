# Python implementation for Git Hooks (prepare-commit-msg and pre-push)

This is an implementation for Git Hooks made with Python.


**IMPORTANT:** To use the scripts it is *necessary* to have a version of **Python 3** installed on your machine.

---

## What was done?

The files **prepare-commit-msg** and **pre-push** (for more details about it, check the [git hooks documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)) were modified to use Python.

### prepare-commit-msg

For each commit the script is called. Basically there is a verification if the commit message is in the defined patterns. We set our patterns as:

* Needs to initiate with feat, chore, test or bug
* Needs to reference, at the end of the message, an open issue and marked with a "doing" label, like this: "(#4)"

Some examples:

```
git commit -m "feat: implements delete user function (#6)"
```
```
git commit -m "test: tests user class (#16)"
```
```
git commit -m "bug: fix the insert task bug (#22)"
```

> Simple. Like. That. :grin:

But, you can also define you own patterns, for sure. All you need to do is change the line 36:

```
regex = '^(feat|hotfix|chore|test):.* \(#[0-9]+\)$'
```

But, keep in mind that the rest of the code depends on the patterns.

### pre-push

Before each push, the script makes some comments on the issue of each commit involved in the operation.

For each commit, a comment with author's name, date and time, changed files and the description of the commit is made in the correspondig issue.

Be like:

![Comment](.github/commit-comment.png)

And, for each push, a comment with author's name, date and time and number of commits.

Be like:

![Comment](.github/push-comment.png)

## How it works

First of all you need to create a [github personal acces token](https://github.com/settings/tokens) to use it. Place it in the variables inside the scripts:

```
USERNAME = 'vitumenezes'
TOKEN = 'Token 4Tby&8202&89#rfwtInNSUUnby&82'
```
> :warning: Need to be like this: 'Token *your_acess_token*'.

The, just copy the python script to corresponding script inside ```.git/hooks/``` where the example files that git offers are usually located.

> :warning: **NOTE:** remove the file extension for the script to work. Your file must be like ```prepare-commit-msg``` **and not** ```prepare-commit-msg.py``` or ```prepare-commit-msg.example```.

---

## That's it! Want to contribute?

- Make a fork of this repo;
- Create a branch with your feature: `git checkout -b my-feature`;
- Commit your changes: `git commit -m 'feat: my new feature'`;
- Push your new branch: `git push origin my-feature`.

> **NOTE**: as you can see, i didn't recommend the patterns with git hooks, it's up to you. If you want to use it, it's great for training :smiley:

## License

This project is under MIT license. See the file [LICENSE](LICENSE.md) for more information.
