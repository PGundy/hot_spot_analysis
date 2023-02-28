# Workflow For Poetry (repo -> Pypi)

This is Philip Gundy's notes on his personal (imperfect) workflow with poetry.

## Key Files
* pyproject.toml - This is where we set macr0-level requirements (python versions, etc.)
* README.MD - This should have an introduction to Hot Spot Analysis (HSA) and a simple example
* hot_spot_analysis_demo.py - this is just a place to test our changes on a very basic HSA use case.


## Poetry workflow
01. open console, nagivate to the repo location: `cd ~/HOT_SPOT_ANALYSIS/`
02. run `poetry list` to ensure poerty is setup properply
03. check which poetry env you are using, and ensure it is the correct python version: `poetry env list`
    1.  If not change environments: `poetry env use <FULL PATH TO ALTERNATIVE ENV>`
    2.  if you don't know the path then run `poetry env info` and use that path to navigate to the desired exec path
4.  run `poetry update`
5.  11. run `pytest` <- ensure all tests pass
6.  run `poetry version` 
7.  run `poetry check`
8.  run `poetry build`
9.  run `poetry check`
10. run `poetry show`
11. run `poetry export` <- not strictly needed because the dependancies are NOT locked
12. Export to PyPi test site: `https://test.pypi.org/project/hot-spot-analysis/`
    1.  Ensure environment variables are working:
        1.  `$TEST_PYPI_USERNAME` & `$TEST_PYPI_PASSWORD`
            1.  `export TEST_PYPI_USERNAME=pgundy93_test`
            2. NOTE: PASSWORD is an API token! `export TEST_PYPI_PASSWORD=1HSAteat!`
13. run `poetry publish -r testpypi --username $TEST_PYPI_USERNAME --password $TEST_PYPI_PASSWORD` <- BIG STEP
    1.  Check PyPi test: `https://test.pypi.org/project/hot-spot-analysis/`

14. continue to repeat and bump the version up in the ``project.toml` file.

15. TODO: replace this with the actual command to publish the package to PyPi proper
