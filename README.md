# Git Commit Hooks

A collection of Git commit hooks generalized from prior projects.

## Build Sphinx Docs & Update

Let's assume you're working on a Python project and using `Sphinx` to generate
documentation. Keeping documentation up-to-date as a code base changes is quite
tedious to do by hand. Two basic ways to automate this task are as follows;
build docs as CI/CD system artifacts or write a script to build docs when a code
base is updated.

This hook takes the latter option -- documentation is re-built whenever commits
are made.

[Check it Out here](./build_docs/build_and_update_sphinx_docs.md)

## Super Lint-Hammer

Imagine the scenario; you're in a group where someone has discovered `pylint`
and decided all commits to production need to have score X/10 in order to pass review.

While linting as part of refactoring is quite helpful, it can be frustrating when
`pylint` is used with default settings and a numeric pass/fail criteria is established.

Enter the _Super Lint-Hammer_ -- a commit hook that will run `autopep8` on every
`*.py` file in the Git repo. While this won't fix fundamental problems with a code base,
it will make things more compliant with PEP8 standards and usually import `pylint` scores
significantly.

[Check it Out here](./build_docs/lint_hammer.md)
