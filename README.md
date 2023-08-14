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

## Usage
### `lunch.py`
```bash
# asdf
asdf install python latest

# asdf local version of python
asdf local latest

# run app in poetry
poetry env use latest
poetry shell
python lunch.py
```

### Poetry
```bash
# Install
curl -sSL https://install.python-poetry.org | $(which python3) -

# Change config
poetry config virtualenvs.in-project true           # .venv in `pwd`

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
docker exec -it lunch bash

# run command inside container
python lunch.py

# destroy container
docker-compose down
```

#### Docker Troubleshooting
* Watch logs in real-time: `docker-compose logs -tf --tail="50" hello`

## Packaging
Local test [pypiserver](https://github.com/pypiserver/pypiserver) and [official repo](https://pypi.org).

**NOTE**  
Confirm repo name is [available](https://pypi.org/help/#project-name) before uploading to PyPi.

```bash
## BOTH
# build package
poetry build

## DOCKER
# setup mount directory
mkdir -p auth

# use passlib to setup .htpasswd
htpasswd -sc auth/.htpasswd someuser

# run local pypi
docker run -p 80:8080 -v $(pwd)/auth/:/data/auth pypiserver/pypiserver:latest -P /data/auth/.htpasswd -a update,download,list /data/packages

# configure repo
poetry config repositories.test http://localhost

# "upload" package to docker
poetry publish -r test

## PYPI
# "upload" package to pypi (build switch is optional)
export API_TOKEN=super_secret_api_key
poetry publish -u __token__ -p $API_TOKEN --build
```

## TODO
* QA
  * macOS 12.1
    * `List All` button doesn't scroll down list
* Document
* Convert to ~~PySimpleGUI~~ NiceGUI
* Extend
  * Fancy category
  * Images
  * Menus
  * API calls to Yelp, Google, etc.
  * Tinder swipe right/left mechanic hehehe

## Further Reading
[Python Poetry, finally easy build and deploy packages | by Jose Alberto Torres Agüera | Lambda Automotive | Medium](https://medium.com/lambda-automotive/python-poetry-finally-easy-build-and-deploy-packages-e1e84c23401f)  

[Python 101: Developing Package with Poetry | by Julio Anthony Leonard | Bootcampers | Medium](https://medium.com/bootcampers/python-101-developing-package-with-poetry-449c57690350)
