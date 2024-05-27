# Introduction
This document is meant to help with the variety of tools and processes to update the `hot_spot_analysis` package.

## Pre-reqs

TODO:
### 1. pyenv environment
This is how we handle version control and testing specific python versions, etc.

**Create venvs with pyenv**
`pyenv versions` # list all pyenv versions
`pyenv install 3.XX` # to add a new version of python
`pyenv virtualenv 3.XX py3_XX` # create a venv of that version of python
`pyenv activate py3_XX` # activate the venv

**Install packages**
`cd your_repo`
`pip install <any_package>` # install packages as you need them
`pip install -r requirements.txt` # Alternatively, install from the repo's requirements.txt

### 2. pyproject.toml
This governs the project's version, required dependancies, etc.

**Control the project version -- be careful when doing this**

**Dependency Management is done here!**
1. Dependancies should be using `>=`
2. Dependancies should be using the oldest compatible version as possible

### 3. locally test the package

`python -m build`
`pip install dist/hot_spot_analysis-0.1.0.tar.gz --force-reinstall` #Note: this should match your desired version
`pip install -e .` # Run in the root of the project, and changes will be reflected immediately
`pytest`


### 4. upload to test pypi
 *ONLY DO THIS AFTER RUNNING TESTS & CONFIRMING FUNCTIONALITY*
`pip install twine`

`python3 -m twine upload --repository testpypi dist/*`
`python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-package-YOUR-USERNAME-HERE`

`twine upload dist/*`

