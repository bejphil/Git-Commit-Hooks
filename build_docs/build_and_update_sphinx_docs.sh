#!/bin/bash

# Identify the root directory for the current Git repo.
TOP_LEVEL_DIR="$(dirname $(git rev-parse --git-dir))"
# We assume the Sphinx files are located in a directory called '/docs/' under the
# root directory
DOCS_DIR="$TOP_LEVEL_DIR/docs/"
# We also assume Sphinx docs use separate build and source directories
DOCS_SOURCE="$DOCS_DIR/source"
DOCS_BUILD="$DOCS_DIR/build"

# Activate a virtual environment and re-build the package
VENV_SOURCE="$TOP_LEVEL_DIR/env/bin/activate"
source $VENV_SOURCE

# Re-install the current python package to make sure all objects are up-to-date
PYTHON_PACKAGE_ROOT="$TOP_LEVEL_DIR"
pip install --upgrade --force-reinstall --no-deps $PYTHON_PACKAGE_ROOT

# Re-build the docs
sphinx-build -b html $DOCS_SOURCE $DOCS_BUILD

# Sync the newly built docs with the S3 bucket
S3_BUCKET="s3://your_s3_bucket_here/"
aws s3 sync $DOCS_BUILD $S3_BUCKET --acl public-read
