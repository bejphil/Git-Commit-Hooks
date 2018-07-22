# Build and Update Sphinx Docs

## Intro

The following hook allows Python `Sphinx` documentation to be re-built and updated
whenever a commit is made.

There are a few assumptions made about the Python project's structure:

* The project has a `setup.py` file in the root directory and can be built using `distutils`.
* There is a virtual environment present in `./env/`.
* Sphinx docs are present in separate source and build directories located at `./docs/source` and `./docs/build`
* Completed docs are hosted in an AWS S3 bucket that the user has write access to.

## Script Structure

First we need to identify the root of the Git repository, which we assume
is where the root of the package is located, along with the directories containing
the Sphinx documentation.

```shell
# Identify the root directory for the current Git repo.
TOP_LEVEL_DIR="$(dirname $(git rev-parse --git-dir))"
# We assume the Sphinx files are located in a directory called '/docs/' under the
# root directory
DOCS_DIR="$TOP_LEVEL_DIR/docs/"
# We also assume Sphinx docs use separate build and source directories
DOCS_SOURCE="$DOCS_DIR/source"
DOCS_BUILD="$DOCS_DIR/build"
```

Next we will activate the virtual environment and re-install the project package.

```shell
# Activate a virtual environment and re-build the package
VENV_SOURCE="$TOP_LEVEL_DIR/env/bin/activate"
source $VENV_SOURCE

# Re-install the current python package to make sure all objects are up-to-date
PYTHON_PACKAGE_ROOT="$TOP_LEVEL_DIR"
pip install --upgrade --force-reinstall --no-deps $PYTHON_PACKAGE_ROOT
```

Now that everything is up to date, we can re-build the docs and update our S3 bucket.

```shell
# Re-build the docs
sphinx-build -b html $DOCS_SOURCE $DOCS_BUILD

# Sync the newly built docs with the S3 bucket
S3_BUCKET="s3://your_s3_bucket_here/"
aws s3 sync $DOCS_BUILD $S3_BUCKET --acl public-read
```
