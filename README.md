# Nameless Deploy Tools

[![Build Status](https://api.travis-ci.com/NitorCreations/nameless-deploy-tools.svg?branch=master)](https://app.travis-ci.com/github/NitorCreations/nameless-deploy-tools/)
[![Coverage Status](https://coveralls.io/repos/github/NitorCreations/nameless-deploy-tools/badge.svg?branch=master)](https://coveralls.io/github/NitorCreations/nameless-deploy-tools?branch=master)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Released version 1.323

Nameless deploy tools are a set of tools to implement a true Infrastructure As Code workflow
with various cloud infrastructure management tools. Currently supported tools are
CloudFormation, AWS CDK, Serverless Framework, Terraform, Azure Resource Manager (with
a YAML syntax) and Bicep.

## Why Nameless?

A common analogy for cloud infrastructure has been to move from having pets with
names that need lots of looking after, to cattle that has at most id's. It's time
to move to the industrial age from the agrarian era. The infrastructure our
applications runs now comes and goes, and we know at most some statistical information
about the actual executions. Run times, memory usage, used bandwidth and the like.
We no longer know even the id's of the things that actually run the code. Hence -
nameless.

## Rationale

We at Nitor are software engineers with mostly a developer or architect background, but
a lot of us have had to work closely with various Operations teams around the world.
DevOps has a natural appeal to us and immediately "infrastructure as code" meant for us
that we should apply the best development practices to infrastructure development. It starts
with version control and continues with testing new features in isolation and a workflow
that supports this. Our teams usually take into use a feature branch workflow if it is
feasible, and we expect all the tools and practices to support this. For infrastructure
this type of branching means that you should be able to spin up enough of the infrastructure
to be able to verify the changes you want to implement in production. Also, the testing
environment should be close enough to the target environment for the results to be valid.
So the differences between testing and production environments should be minimized and
reviewable.

With the popular tools like Ansible, Terraform, Chef etc. you need to come up with and
implement the ways to achieve the goals above. As far as I know, no tool besides ndt
has at its core a thought-out way of a branching infrastructure development model.

## What it is

nameless-deploy-tools works by defining _Amazon Machine Images_, _[Docker containers](https://www.docker.com)_,
_[Serverless services](https://serverless.com)_ and deploying _[CloudFormation](https://aws.amazon.com/cloudformation/)
stacks_ of resources. CloudFormation stacks can also be defined with _[AWS CDK](https://awslabs.github.io/aws-cdk/)_
applications. All of the above can also be deployed using _[Terraform](https://www.terraform.io)_.

## Installation

Requires Python 3.8 or newer.

```shell
pip install nameless-deploy-tools
```

Or in an isolated environment using [pipx](https://github.com/pypa/pipx):

```shell
pipx install nameless-deploy-tools
pipx upgrade nameless-deploy-tools
```

## Getting started

To use nameless-deploy-tools you need to set up a _project repository_ that
describes the images you want to build, and the stacks you want to deploy them in. See
[ndt-project-template](https://github.com/NitorCreations/ndt-project-template)
for an example.

Here are few commands you can use. All of these are run in your project repository root.
You need to have AWS credentials for command line access set up.

* To bake a new version of an image: `ndt bake-image <image-name>`
* To build a new Docker container image `ndt bake-docker <component> <docker-name>`
* To deploy a stack:
  * with a known AMI id: `ndt deploy-stack <image-name> <stack-name> <AMI-id>`
  * with the newest AMI id by a given bake job: `ndt deploy-stack <image-name> <stack-name> "" <bake-job-name>`
* To undeploy a stack: `ndt undeploy-stack <image-name> <stack-name>`

For full list of commands see [here](docs/commands.md)

### Faster shell complete

You can additionally use a faster register-complete by running `./faster_register_complete.sh`.
This compiles C++ programs from the files
[n_utils/nameless-dt-register-complete.cpp](n_utils/nameless-dt-register-complete.cpp)
and [n_utils/nameless-dt-print-aws-profiles.cpp](n_utils/nameless-dt-print-aws-profiles.cpp),
and replaces the Python versions of `nameless-dt-register-complete`
and `nameless-dt-print-aws-profiles` with these much faster compiled binaries.

## Documentation

* [Command Reference](docs/commands.md)
* [ndt workspace tooling](docs/workspace.md)
* [Template Pre-Processing](docs/template-processing.md)
* [Multifactor Authentication](docs/mfa.md)
* [Common parameters](docs/parameters.md)

## Versioning

This library uses a simplified semantic versioning scheme: major version change for changes
that are not backwards compatible (not expecting these) and the minor
version for all backwards compatible changes. We won't make the distinction between
new functionality and bugfixes, since we don't think it matters and is not a thing
worth wasting time on. We will release often and if we need changes that are not comptatible,
we will fork the next major version and release alphas versions of that until we are
happy to release the next major version and try and have a painless upgrade path.

## Dependencies

Python dependencies are specified in [pyproject.toml](./pyproject.toml).
[pip-compile](https://github.com/jazzband/pip-tools/) is used to generate the `requirements.txt` file.
To update the requirements, use the following commands:

```shell
pipx install pip-tools
pip-compile pyproject.toml
```

Dev and test requirements are specified separately:

```shell
# This will output the requirements for the "dev" and "testing" groups
pip-compile --all-extras --output-file=dev-requirements.txt --strip-extras pyproject.toml
```

Use the helper script to automatically run pip-compile:

```shell
./compile-requirements.sh
```

## Running tests

Install test requirements:

```shell
pip install -r dev-requirements.txt
```

Run tests with Pytest:

```shell
python -m pytest -v .
```

## Code formatting and linting

This project uses [ruff](https://github.com/astral-sh/ruff)
together with [isort](https://github.com/PyCQA/isort) for Python code formatting and linting.
They are configured with a custom line length limit of 120.

Usage:

```shell
pipx install isort ruff
isort .
ruff check --fix .
ruff format .
```

Using with [pre-commit](https://pre-commit.com/):

```shell
# setup to be run automatically on git commit
pre-commit install

# run manually
pre-commit run --all-files
```
