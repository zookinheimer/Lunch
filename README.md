# Lunch

[@zookinheimer's](https://github.com/zookinheimer/Lunch/commits?author=zookinheimer) masterpiece. Gonna fill in the blanks and/or add tooling.

— [@pythoninthegrass](https://github.com/pythoninthegrass)

## Setup
* Install 
    # [asdf](https://asdf-vm.com/guide/getting-started.html)
    * [poetry](https://python-poetry.org/docs/)
    * [docker-compose](https://docs.docker.com/compose/install/)
    * [editorconfig](https://editorconfig.org/)
    * [playwright](https://playwright.dev/python/docs/intro#installation)

## Usage
### `lunch.py`
```bash
# install tkinter library on macos
brew install python-tk

# asdf
asdf install python 3.9

# asdf local version of python
asdf local 3.9.10

# run app in poetry
poetry env use 3.9.10
poetry shell
python lunch.py
```

### Poetry
```bash
# Install
curl -sSL https://install.python-poetry.org | $(which python3) -

# Change config
poetry config virtualenvs.in-project true           # .venv in `pwd`
poetry config experimental.new-installer false      # fixes JSONDecodeError on Python3.10

# Activate virtual environment (venv)
poetry shell

# Deactivate venv
exit  # ctrl-d

# Install multiple libraries
poetry add google-auth google-api-python-client

# Initialize existing project
poetry init

# Run script and exit environment
poetry run python your_script.py

# Install from requirements.txt
poetry add `cat requirements.txt`

# Update dependencies
poetry update

# Remove library
poetry remove google-auth

# Generate requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Docker
```bash
# clean build (remove `--no-cache` for speed)
docker-compose build --no-cache --parallel

# start container
docker-compose up --remove-orphans -d

# exec into container
docker attach hello

# run command inside container
python hello.py

# destroy container
docker-compose down
```

#### Docker Troubleshooting
* Watch logs in real-time: `docker-compose logs -tf --tail="50" hello`
* Check exit code
    ```bash
    $ docker-compose ps
    Name                          Command               State    Ports
    ------------------------------------------------------------------------------
    docker_python      python manage.py runserver ...   Exit 0
    ```

## TODO
* ~~Add README.md~~
* ~~PR~~
* ~~Clone~~
* QA
    * Excluded `lunch.db` in `.gitignore`
        * Will pollute original DB with future commits
        * Possibly add a separate shell script to populate robust sqlite DB
    * macOS 12.1
        * Changed `root.geometry` to `"500x100"`
        * Arbys [sic] seems to be the only cheap restaurant available
            * Have to reset by selecting normal
        * `List All` button doesn't scroll down list
* Document
* Extend
    * Fancy category
    * Images
    * Menus
    * API calls to Yelp, Google, etc.
    * Faithful tkinter translation via
        * [Dart](https://dart.dev/)
        * [Flask](https://flask.palletsprojects.com/en/2.0.x/)
        * [Kotlin](https://kotlinlang.org/)
        * [Svelte](https://svelte.dev)
    * Tinder swipe right/left mechanic hehehe
