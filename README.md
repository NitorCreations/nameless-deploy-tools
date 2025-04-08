# Nameless Deploy Tools

[![Build Status](https://api.travis-ci.com/NitorCreations/nameless-deploy-tools.svg?branch=master)](https://app.travis-ci.com/github/NitorCreations/nameless-deploy-tools/)
[![Coverage Status](https://coveralls.io/repos/github/NitorCreations/nameless-deploy-tools/badge.svg?branch=master)](https://coveralls.io/github/NitorCreations/nameless-deploy-tools?branch=master)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Released version 1.331

Nameless deploy tools are a set of tools to implement a true Infrastructure As Code workflow
with various cloud infrastructure management tools.
Currently supported tools are:

- CloudFormation
- AWS CDK
- Serverless Framework
- Terraform
- Azure Resource Manager (with YAML syntax)
- Bicep

## Why Nameless?

A common analogy for cloud infrastructure has been to move from having pets with
names that need lots of looking after, to cattle that has at most id's.
It's time to move to the industrial age from the agrarian era.
The infrastructure our applications runs now comes and goes,
and we know at most some statistical information about the actual executions.
Run times, memory usage, used bandwidth and the like.
We no longer know even the id's of the things that actually run the code.
Hence - nameless.

## Rationale

We at Nitor are software engineers with mostly a developer or architect background,
but a lot of us have had to work closely with various Operations teams around the world.
DevOps has a natural appeal to us and immediately "infrastructure as code" meant for us
that we should apply the best development practices to infrastructure development.
It starts with version control and continues with testing new features in isolation and a workflow that supports this.
Our teams usually take into use a feature branch workflow if it is feasible,
and we expect all the tools and practices to support this.
For infrastructure this type of branching means that you should be able to spin up enough of the infrastructure
to be able to verify the changes you want to implement in production.
Also, the testing environment should be close enough to the target environment for the results to be valid.
So the differences between testing and production environments should be minimized and reviewable.

With the popular tools like Ansible, Terraform, Chef etc.
you need to come up with and implement the ways to achieve the goals above.
As far as I know, no tool besides ndt has at its core a thought-out way of a branching infrastructure development model.

## What it is

nameless-deploy-tools works by defining _Amazon Machine Images_,
_[Docker containers](https://www.docker.com)_,
_[Serverless services](https://serverless.com)_,
and deploying _[CloudFormation](https://aws.amazon.com/cloudformation/)
stacks_ of resources. CloudFormation stacks can also be defined with _[AWS CDK](https://awslabs.github.io/aws-cdk/)_
applications. All of the above can also be deployed using _[Terraform](https://www.terraform.io)_.

## Installation

Requires Python 3.9 or newer.

Use pipx or uv to install it globally in an isolated environment.
[pipx](https://github.com/pypa/pipx) is the older and stable tool,
[uv](https://github.com/astral-sh/uv) is a new, much faster version.

```shell
pipx install nameless-deploy-tools
# or
uv tool install nameless-deploy-tools
```

Directly installing with pip is no longer supported by most Python distributions.

## Getting started

To use nameless-deploy-tools you need to set up a _project repository_ that
describes the images you want to build, and the stacks you want to deploy them in.
See [ndt-project-template](https://github.com/NitorCreations/ndt-project-template) for an example.

Here are few commands you can use. All of these are run in your project repository root.
You need to have AWS credentials for command line access set up.

- To bake a new version of an image: `ndt bake-image <image-name>`
- To build a new Docker container image `ndt bake-docker <component> <docker-name>`
- To deploy a stack:
  - with a known AMI id: `ndt deploy-stack <image-name> <stack-name> <AMI-id>`
  - with the newest AMI id by a given bake job: `ndt deploy-stack <image-name> <stack-name> "" <bake-job-name>`
- To undeploy a stack: `ndt undeploy-stack <image-name> <stack-name>`

For full list of commands see [here](docs/commands.md)

### Faster shell complete

You can additionally use a faster register-complete by running `./faster_register_complete.sh`.
This compiles C++ programs from the files
[n_utils/nameless-dt-register-complete.cpp](n_utils/nameless-dt-register-complete.cpp)
and [n_utils/nameless-dt-print-aws-profiles.cpp](n_utils/nameless-dt-print-aws-profiles.cpp),
and replaces the Python versions of `nameless-dt-register-complete`
and `nameless-dt-print-aws-profiles` with these much faster compiled binaries.

## Documentation

- [Command Reference](docs/commands.md)
- [ndt workspace tooling](docs/workspace.md)
- [Template Pre-Processing](docs/template-processing.md)
- [Multifactor Authentication](docs/mfa.md)
- [Common parameters](docs/parameters.md)

## Versioning

This library uses a simplified semantic versioning scheme: major version change for changes
that are not backwards compatible (not expecting these) and the minor
version for all backwards compatible changes. We won't make the distinction between
new functionality and bugfixes, since we don't think it matters and is not a thing
worth wasting time on. We will release often and if we need changes that are not comptatible,
we will fork the next major version and release alphas versions of that until we are
happy to release the next major version and try and have a painless upgrade path.

## Development

uv is the recommended way to handle virtual environments for development.

Create a venv and install all dependencies:

```shell
uv sync --all-extras
```

You can then run commands directly with the venv using `uv run`,
or activate the venv manually first.
The uv default venv location is `.venv`.

```shell
source .venv/bin/activate
# or Windows
.venv\Scripts\activate
```

## Dependencies

Python dependencies are specified in [pyproject.toml](./pyproject.toml).
The `requirements.txt` file is generated by pip compile and should not be modified manually.

Use the provided shell script to update the requirements file.
First install [uv](https://github.com/astral-sh/uv) (recommended),
or alternatively `pip-tools` using [pipx](https://github.com/pypa/pipx).
Then run:

```shell
./compile-requirements.sh
# See help
./compile-requirements.sh -h
```

## Running tests

### Using uv

```shell
uv run python -m pytest -v .
```

## Inside active virtual env

Install test requirements:

```shell
pip install -r dev-requirements.txt
```

Run tests with Pytest:

```shell
python -m pytest -v .
```

## Code formatting and linting

Code formatting and linting with [ruff](https://github.com/charliermarsh/ruff).

These are configured with a custom line length limit of 120.
The configs can be found in [pyproject.toml](./pyproject.toml).

Usage:

```shell
ruff format
ruff check --fix
```

Using with [pre-commit](https://pre-commit.com/):

```shell
# setup to be run automatically on git commit
pre-commit install

# run manually
pre-commit run --all-files
```

## Release

Use the provided shell script.
Note that you need to have a venv with the extra dependencies installed active when running the script.

```shell
./release.sh
# See help
./release.sh -h
```
