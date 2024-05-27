# Developer Guide

This guide will help you set up the development environment, build the package, install it locally, and upload it to Test PyPI or PyPI.

## Prerequisites
- Python 3.7+
- `pip` and `virtualenv`
- `setuptools` and `wheel`
- `twine` for uploading the package

## Setting Up Development Environment
1. **Clone the repository:**
```zsh
git clone https://github.com/your_username/your_package.git
cd your_package
```

2. **Create a virtual environment:**
```zsh
pyenv versions                 # list all pyenv versions

# NOTE: No need to install a new version of python if you already have a venv of it!

# pyenv install 3.XX           # install a new version of python
# pyenv virtualenv 3.XX py3_XX # create a venv from that version of python
pyenv activate py3_XX          # activate your version of python
```

3. **Install dependencies:**
```zsh
cd your_package                  # you should already be here 
# pip install <any_package>      # install packages as you need them
pip install -r requirements.txt  # Alternatively, install from the repo's requirements.txt
```

4. **Install development tools**
```zsh
pip install setuptools wheel twine # tools to build package & upload it
```

5. **Package Version Control: pyproject.toml**
This governs the project's version, required dependancies, etc.

            **be careful when doing this**




## Building the Package

**Recommended:** run `test_build_install.py`


```zsh
cd your_package
python -m build # NOTE: the version will be governed from thte project.toml
```

## Installing the Package Locally
```zsh
pyenv activate py3_XX # not required if starting from the top
pip uninstall your_package

cd your_package
pip install dist/<your_package-0.1.0-py3-none-any.whl> # NOTE: update this to your specific version
pip list # Now confirm the correct version is listed
```

## Running unit tests
```zsh
cd your_package
pyenv activate py3_XX

# Note that the package is installed in the previous step!

pytest # this will run all the tests
```

# Uploading the built package

## upload to test pypi

Upload your package to test.pypi.org so that everything is working, and make any mistakes you want!
1. Upload to test.pypi
```zsh
cd your_package
pyenv activate py3_XX

twine upload --repository testpypi dist/*
```

2. Install from test.pypi
```zsh
python3 -m python3 -m pip install -i https://test.pypi.org/simple/ hot-spot-analysis
```


## *USE WITH CAUTION* upload to pypi

***Zero mistakes allowed*** -- test several times with test.pypi first.

```zsh
cd your_package
pyenv activate py3_XX

twine upload dist/*
```