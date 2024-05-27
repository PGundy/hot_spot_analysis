import glob
import logging
import os

import pytest
from pip._internal.cli.main import main as pip_main

import build


class PackageBuilder:
    def __init__(self, project_dir="."):
        self.project_dir = project_dir
        self.dist_dir = os.path.join(project_dir, "dist")
        self.project_name = os.path.basename(os.getcwd())
        logging.basicConfig(level=logging.INFO)

    def build_package(self):
        """Build the package using the build module."""
        try:
            # Build the package in 'dist' directory
            builder = build.ProjectBuilder(self.project_dir)
            sdist_path = builder.build("sdist", self.dist_dir)
            wheel_path = builder.build("wheel", self.dist_dir)
            logging.info("Package built successfully: %s, %s", sdist_path, wheel_path)
        except Exception as e:
            logging.error("Error occurred while building the package: %s", e)
            raise

    def install_wheel(self):
        """Install the wheel file created by the build_package() function."""
        try:
            # Find the wheel file in the 'dist' directory
            wheel_files = glob.glob(os.path.join(self.dist_dir, "*.whl"))
            if not wheel_files:
                raise FileNotFoundError("No wheel file found in 'dist' directory.")

            # Install the first wheel file found
            wheel_file = wheel_files[0]
            #!
            # NOTE: You must uninstall the package in the terminal if you advanced past the current version!
            #!
            print("\n\n\n\n")
            print(f"Attempting to install: {wheel_file}")
            pip_main(["install", wheel_file])
            logging.info("Installed wheel file: %s", wheel_file)
            print("\n\n\n\n")

        except Exception as e:
            logging.error("Error occurred while installing the wheel file: %s", e)
            raise

    def run_tests(self):
        """Run all tests using pytest."""
        try:
            # Run pytest and capture the exit code
            exit_code = pytest.main()
            if exit_code == 0:
                logging.info("All tests passed successfully.")
            else:
                logging.warning("Some tests failed. Exit code: %d", exit_code)
            return exit_code
        except Exception as e:
            logging.error("Error occurred while running tests: %s", e)
            raise


if __name__ == "__main__":
    # Create an instance of PackageBuilder
    builder = PackageBuilder()

    # Step 1: Build the package
    builder.build_package()

    # Step 2: Install the wheel file
    builder.install_wheel()

    # Step 3: Run the tests
    builder.run_tests()
