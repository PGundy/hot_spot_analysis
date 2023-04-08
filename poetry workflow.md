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
    1.  run `pytest` <- ensure all tests pass
5.  run `poetry version` 
6.  run `poetry check`
7.  run `poetry build`
8.  run `poetry check`
9.  run `poetry show`
10. run `poetry export` <- not strictly needed because the dependancies are NOT locked
11. Export to PyPi test site: `https://test.pypi.org/project/hot-spot-analysis/`
    1.  Ensure environment variables are working:
        1.  `$TEST_PYPI_USERNAME` & `$TEST_PYPI_PASSWORD`
            1.  `export TEST_PYPI_USERNAME=pgundy93_test`
            2. NOTE: PASSWORD is an API token! `export TEST_PYPI_PASSWORD=1HSAteat!`
12. run `poetry publish -r testpypi --username $TEST_PYPI_USERNAME --password $TEST_PYPI_PASSWORD --build` <- BIG STEP
    1.  Check PyPi test: `https://test.pypi.org/project/hot-spot-analysis/`

13. continue to repeat and bump the version up in the ``project.toml` file.

14. Upload to PyPi proper
    1.  `poetry publish --build --dry-run`
    2.  `poetry publish --username PGundy93 --password <UPDATE WITH REAL PASSWORD>`
