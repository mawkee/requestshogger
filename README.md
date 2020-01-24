# Requests Hogger

Capture and present potentially any kind of HTTP API requests

## Quickstart

### Using docker/dockerhub

```
docker run -p 8910:8910 mawkee/requestshogger
```

### Using local repository

1. Download or clone this repository
1. Run `pipenv install`
1. Run `pipenv run python hogger/reqhogger.py`

### Usage

By default, RequestsHogger binds to 127.0.0.1 and port 8910. Just submit any kind of request (GET, POST, PUT, DELETE, PATCH, you name it) to `http://127.0.0.1:8910/hog/` and they'll be automatically captured. To see the captured requests, check `http://127.0.0.1:8910/`.

Note that this program is not meant to implement any security at all. It should NEVER be used on any kind of production environment, instead being used solely as a local development or testing tool.

## Configurations

There are a few environment variables that can be used to change the behavior.

- HOGGER_PERSIST
    By default, RequestsHogger will not persist your requests on disk, instead using an in-memory database. This means that in a restart, all your data will be lost. Setting this environment variable to any value will inform RequestsHogger that you want your data to persist on a `hogger.json` file.
    Usage: `HOGGER_PERSIST=1 pipenv run python hogger/reqhogger.py`
- HOGGER_HOST and HOGGER_PORT
    The host and port to bind to. By default, HOST binds to `127.0.0.1` and PORT binds to `8910`. Just change them as you see fit, if necessary
    Usage: `HOGGER_PORT=8888 pipenv run python hogger/reqhogger.py`

## Prerequisites

If you use `pipenv`, the `pipenv install` command will create your venv and install any packages you need. To install pipenv, follow the instructions on [Pipenv's GitHub Page](https://github.com/pypa/pipenv).

If you don't want to use pipenv, you can simply create a new virtual environment in any way you see fit (venv, virtualenvwrapper, etc) and install the packages `cherrypy` and `tinydb`. Those are the only tools necessary for running the project, and since we're only using the basic functions, it should work with any version of those projects.

## Supported Python versions

This project was tested on Python 3.6, 3.7 and 3.8

## Tests

##### TODO - Create tests
Currently there are no tests of any kind for this project

* Running unit tests:

```sh
$ python -m unittest discover -v
```

* Running tests coverage:

```sh
$ coverage run -m unittest discover
$ coverage report -m
$ coverage erase
```

## Built With

* Basic Interface implemented on top of [MDBootStrap](http://mdbootstrap.com)
* Tabular data with [DataTables](http://datatables.net)

## Contributing

Just make sure you use the pre-commit hooks and follow the PEP8 specification. You probably want to install the basic tools as well (black, isort, flake8, etc). For that, just run `pipenv install --dev`.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/mawkee/requ/tags).

## Authors

* **Danilo Martins** - *Initial work* - [Mawkee](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Heavily inspired by [MailHog](https://github.com/mailhog/MailHog/)
