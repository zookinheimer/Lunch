# Lunch

[@zookinheimer's](https://github.com/zookinheimer/Lunch/commits?author=zookinheimer) masterpiece. Gonna fill in the blanks and/or add tooling.

— [@pythoninthegrass](https://github.com/pythoninthegrass)

## Setup
* Install 
  * [asdf](https://asdf-vm.com/guide/getting-started.html)
  * [poetry](https://python-poetry.org/docs/)
  * [docker-compose](https://docs.docker.com/compose/install/)
  * [editorconfig](https://editorconfig.org/)
  * [playwright](https://playwright.dev/python/docs/intro#installation)

## Quickstart

```bash
# clone repo
git clone https://github.com/xBromsson/marley.git

# change directory
cd lunch/

# install dependencies
python -m pip install -r requirements.txt

# run program
python main.py

# quit program
ctrl + c
```

## Development

### Python virtual environment

```bash
# create virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
python -m pip install -r requirements.txt 
```

### Additional tooling

Additional tooling includes but is not limited to:

#### asdf

* Install [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
* Usage
    ```bash
    # add python plugin
    asdf plugin-add python

    # install stable python
    asdf install python <latest|3.11.4>

    # set stable to system python
    asdf global python latest

    # add poetry asdf plugin
    asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

    # install latest version via asdf
    asdf install poetry <latest|1.5.1>

    # set latest version as default
    asdf global poetry latest
    ```

#### poetry

* Install [poetry](https://python-poetry.org/docs/#installation) if not using `asdf`
* Usage
    ```bash
    # use venv in repo
    poetry config virtualenvs.in-project true

    # install dependencies
    poetry install

    # add new dependency
    poetry add <package>

    # remove dependency
    poetry remove <package>

    # activate virtual environment
    poetry shell

    # run program
    python main.py

    # exit virtual environment
    exit
    ```

#### vscode

* Install [vscode](https://code.visualstudio.com/download)
* Setup [vscode settings](.vscode/launch.json)
  * Handles debug settings for generic python programs as well as others (e.g., django, flask, etc.)
* Dev Containers
  * [Command palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) (⇧⌘P) > Dev Containers: Reopen in Container
  * F5 for debug
      * May need to select interpreter (e.g., `/opt/venv/bin/python`) first

#### ruff

* Installed via `poetry` or `pip`
* Add VSCode plugin for [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
  * **Optional**: disable pylance in favor of ruff in [repo settings](.vscode/settings.json)
    ```json
    "python.analysis.ignore": [
      "*"
    ],
    ```
* Usage
    ```bash
    # run linter
    ruff check <.|main.py>      # `--fix` arg to use a one-liner 

    # run linter and fix issues
    ruff fix .

    # run tests
    ruff

    # run tests with coverage
    ruff --coverage

    # run tests with coverage and open in browser
    ruff --coverage --open
    ```

#### pre-commit

```bash
# install pre-commit dev dependency
poetry install

# install pre-commit hooks
pre-commit install

# update
pre-commit autoupdate
```

#### editorconfig

Handles formatting of files. [Install the editorconfig plugin](https://editorconfig.org/#download) for your editor of choice.

#### dependabot

* [Dependabot](https://dependabot.com/) is a GitHub tool that automatically creates pull requests to keep dependencies up to date.

## TODO

* QA
  * Desktop
    * macOS: `native` form input is broken bc `pywebview`
    * Linux
    * Windows
  * Mobile
    * iOS
    * Android
* Document
* ~~Convert to ~~PySimpleGUI~~ NiceGUI~~
* Extend
  * [semantic-release](https://github.com/semantic-release/semantic-release)
  * sqlite -> postgres
  * Fancy category
  * Images
  * Menus
  * API calls to Yelp, Google, etc.
  * Tinder swipe right/left mechanic hehehe

## Further Reading

[Python Poetry, finally easy build and deploy packages | by Jose Alberto Torres Agüera | Lambda Automotive | Medium](https://medium.com/lambda-automotive/python-poetry-finally-easy-build-and-deploy-packages-e1e84c23401f)  

[Python 101: Developing Package with Poetry | by Julio Anthony Leonard | Bootcampers | Medium](https://medium.com/bootcampers/python-101-developing-package-with-poetry-449c57690350)
