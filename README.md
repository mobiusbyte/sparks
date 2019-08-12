# Sparks
<!-- insert badges here -->
Sparks is a minimal command-line tool to manage customizable project folders from templates.

## Features
* Simple command line usage thanks to [Click](https://click.palletsprojects.com).
* Customizable folder, files, and file contents thanks to [Jinja2](http://jinja.pocoo.org).

<!--
## Table of Contents
Optionally, include a table of contents in order to allow other people to quickly navigate especially long or detailed READMEs.
-->
## Installation
Run the following to install:
```bash
pip install sparks
```

## Usage

### Creating a new project
```bash
sparks create --help
Usage: sparks create [OPTIONS]

Options:
  -t, --template TEXT  Template folder to generate from
  -o, --output TEXT    Output folder to create files in. The folder will be
                       created if it does not already exist.
  --skip-prompt        Skips the prompt and uses the default settings as
                       specified in the spark_config.yaml.
  --help               Show this message and exit.
```


## Contributing

### Development setup
1. Install `pipenv`
	```bash
	pip install pipenv
	```
2. Clone this repository and activate your environment
	```bash
	bash-3.2$ git clone git@github.com:binaryart/sparks.git
	bash-3.2$ cd sparks
	bash-3.2$ pipenv shell
	(sparks) bash-3.2$ pipenv install --dev
	(sparks) bash-3.2$ pre-config install
	```
3. Make your changes in the application and test code
4. Run the tests
	```bash
	(sparks) bash-3.2$ pytest test
	```
5. Commit your changes. The commit will fail if any of the `pre-commit` rules failed their check. Simply follow the instructions from the console to fix the check failures.

### Publishing
1. Bump the version in `setup.py`
2. Merge this change to `master` branch
3. Generate the distribution packages and upload it to PyPI
	```bash
	(sparks) bash-3.2$ python setup.py bdist_wheel sdist
	(sparks) bash-3.2$ twine upload dist/*
	```

<!--
## Credits
Include a section for credits in order to highlight and link to the authors of your project.
-->

## License
Sparks is released under the [MIT License](https://opensource.org/licenses/MIT).

