# Developer Guide

This guide will help you set up the development environment, build the package, install it locally, and upload it to Test PyPI or PyPI.

## Prerequisites
- Python 3.7+
- `pip` and `virtualenv`
- `setuptools` and `wheel`
- `twine` for uploading the package

## Setting Up Development Environment & local installation
1. **Clone the repository:**
```zsh
git clone https://github.com/your_username/your_package.git
cd path/to/your_package
```

2. **Create a virtual environment:**
```zsh
pyenv versions                 # list all pyenv versions

# NOTE: No need to install a new version of python if you already have a venv of it!

# pyenv install 3.XX           # install a new version of python
# pyenv virtualenv 3.XX py3_XX # create a venv from that version of python
pyenv activate py3_XX          # activate your version of python
```

3. **Install development tools to your venv**
```zsh
pip install build pytest setuptools twine wheel # tools to test, build, and upload the package
```

4. **Manage the package via pyproject.toml** 
This file governs the project's version, required dependancies, etc. Be careful when eddting this file.

Some Helpful Reminders:
1. You cannot upload the same version twice (EVER), so ensure the package passes tests locally in a new venv before building & uploading!
2. version = "X.X.Xa" will release vX.X.X in pre-release 'a'! 
3. Always upload in pre-release first to ensure versions incriment as intended!


5. **Install the requirements & package locally:**
```zsh
cd path/to/your_package          # you should already be here 
# pip install <any_package>      # install packages as you need them

# Optionally 
pip install pyproject.toml # install dependencies
```


6. **Installing the Package Locally**
```zsh
pyenv activate py3_XX # not required if starting from the top
pip uninstall your_package

cd path/to/your_package
pytest # run all unit tests, only install locally if all unit tests pass. Otherwise resolve failures.

pip install -e . # NOTE: update this to your specific version
pip list # Now confirm the correct version is listed
```

7. **Optional: Test the local package in a new venv**
```zsh

# NOTE: This example uses python 3.9, but any version of python can be used.

pyenv versions                          # list installed python versions
#pyenv install 3.9                      # Optional, install python 3.9 if not already

pyenv virtualenv-delete py3_9_test_env  # delete venv if it exsists
pyenv virtualenvs                        # list current venvs

pyenv virtualenv 3.9 py3_9_test_env     # create venv
pyenv activate py3_9_test_env           # activate the new venv

cd path/to/your_package     # go to package dir

pip install -r build_requirements.txt   # install build dependencies
pip install pyproject.toml              # install dependencies

pytest                      # Run unit tests to confirm state of package

pip install -e .            # Install package locally
pip list                    # Confirm version of installed package

## TODO: Run any scripts, tests, example files to confirm working state of the package in fresh venv!

pyenv virtualenv-delete py3_9_test_env   # delete the venv

```


# Build the package
1. **Run unittests (successfully)**
```zsh
cd path/to/your_package
pyenv activate py3_XX

pytest # this will run all the tests, and resolve any errors before building.
```

2. **Building the Package**
```zsh
# Note: This requires the 6 above steps to be run!

cd path/to/your_package
python -m build # NOTE: Package version & requirements are specified in the `project.toml`

# And now we have the package files!
```


# Uploading the package
## Upload to test.pypi (test release)

1. **Upload to test.pypi.org**

Upload your package to test.pypi.org so that everything is working, and make any mistakes you want!
```zsh
cd path/to/your_package
pyenv activate py3_XX

twine upload --repository testpypi dist/*
```


2. **Upload to pypi (official release)**

***Zero mistakes allowed*** -- test several times with test.pypi first.

```zsh
cd path/to/your_package
pyenv activate py3_XX

twine upload dist/*
```