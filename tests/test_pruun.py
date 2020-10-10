import os
import subprocess

from click.testing import CliRunner
from pruun.commands import pruun
from pruun.utils import get_dependency_names


def test_passing_single_handler_path():
    """
    Scenario: single handler_path arg passed.
    Test parsing of installed packages, creation of .zip, and finally validate integrity of .zip.
    """
    runner = CliRunner()
    lambda_file_name = "handler.py"
    package_name = "deployment_package.zip"

    with runner.isolated_filesystem():
        with open(lambda_file_name, "w") as f:  # create dummy lambda handler file
            pass

            result = runner.invoke(pruun, ["package", lambda_file_name])

            # check for no exceptions
            assert result.exit_code == 0

            # check for existence of .zip file
            assert os.path.isfile(package_name) == True

            # verify integrity of .zip
            depens = get_dependency_names()
            for depen in depens:
                underscored_name = depen.replace("-", "_").strip()
                cmd = f"unzip -l {package_name} {underscored_name}*"
                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    check=True,
                )  # check .zip for all installed packages

            cmd = f"unzip -l {package_name} {lambda_file_name}"
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,
            )  # check .zip for lambda handler file

            f.close()


def test_multiple_handler_paths():
    """
    Scenario: multiple handler_paths args passed.
    Test parsing of installed packages, creation of .zip, and finally validate integrity of .zip.
    """
    runner = CliRunner()
    lambda_file_name = "handler.py"
    dependency_file_a = "a.py"
    dependency_file_b = "b.py"
    package_name = "deployment_package.zip"

    with runner.isolated_filesystem():
        with open(lambda_file_name, "w") as f, open(dependency_file_a, "w") as f2, open(
            dependency_file_b, "w"
        ) as f3:  # create dummy lambda handler file
            pass

            result = runner.invoke(
                pruun,
                ["package", lambda_file_name, dependency_file_a, dependency_file_b],
            )

            # check for no exceptions
            assert result.exit_code == 0

            # check for existence of .zip file
            assert os.path.isfile(package_name) == True

            # verify integrity of .zip
            depens = get_dependency_names()
            for depen in depens:
                underscored_name = depen.replace("-", "_").strip()
                cmd = f"unzip -l {package_name} {underscored_name}*"
                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    check=True,
                )  # check .zip for all installed packages

            cmd = f"unzip -l {package_name} {lambda_file_name} {dependency_file_a} {dependency_file_b}"
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,
            )  # check .zip for lambda handler file

            f.close()


def test_lambda_directory_support():
    """
    Scenario: single directory handler_path arg passed.
    Similar to test_deployment_package_creation(), except a directory path is passed as the value for `handler_path`.
    """
    runner = CliRunner()
    lambda_file_name = "handler.py"
    package_name = "deployment_package.zip"

    with runner.isolated_filesystem():

        # create dummy dir to containg lambda application code
        lambda_dir_name = "lambda_dir/"
        lambda_dir_path = os.path.join(os.getcwd(), lambda_dir_name)
        os.mkdir(lambda_dir_path)

        lambda_file_path = os.path.join(lambda_dir_path, lambda_file_name)
        with open(lambda_file_path, "w") as f:  # create dummy lambda handler file
            pass

            result = runner.invoke(pruun, ["package", lambda_dir_name])

            # check for no exceptions
            assert result.exit_code == 0

            # check for existence of .zip file
            assert os.path.isfile(package_name) == True

            # verify integrity of .zip
            depens = get_dependency_names()
            for depen in depens:
                underscored_name = depen.replace("-", "_").strip()
                cmd = f"unzip -l {package_name} {underscored_name}*"
                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    check=True,
                )

            cmd = f"unzip -l {package_name} {lambda_dir_name}"
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,
            )  # check .zip for lambda handler file

            f.close()
