import os
import subprocess

from click.testing import CliRunner
from pruun.commands import pruun
from pruun.utils import get_dependency_names


def test_deployment_package_creation():
    """
    Test parsing of installed packages, creation of .zip, and finally validate integrity of .zip.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("handler.py", "w") as f:  # create dummy lambda handler file
            pass

            result = runner.invoke(pruun, ["package", "handler.py"])

            # check for no exceptions
            assert result.exit_code == 0

            # check for existence of .zip file
            assert os.path.isfile("deployment_package.zip") == True

            # verify integrity of .zip
            depens = get_dependency_names()
            for depen in depens:
                underscored_name = depen.replace("-", "_").strip()
                cmd = f"unzip -l deployment_package.zip {underscored_name}*"
                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    check=True,
                )

            f.close()


def test_lambda_directory_support():
    """
    Similar to test_deployment_package_creation(), except a directory path is passed as the value for `handler_path`.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():

        # create dummy dir to containg lambda application code
        lambda_dir_path = os.path.join(os.getcwd(), "lambda_dir")
        os.mkdir(lambda_dir_path)

        lambda_file_path = os.path.join(lambda_dir_path, "handler.py")
        with open(lambda_file_path, "w") as f:  # create dummy lambda handler file
            pass

            result = runner.invoke(pruun, ["package", lambda_dir_path])

            # check for no exceptions
            assert result.exit_code == 0

            # check for existence of .zip file
            assert os.path.isfile("deployment_package.zip") == True

            # verify integrity of .zip
            depens = get_dependency_names()
            for depen in depens:
                underscored_name = depen.replace("-", "_").strip()
                cmd = f"unzip -l deployment_package.zip {underscored_name}*"
                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    check=True,
                )

            f.close()
