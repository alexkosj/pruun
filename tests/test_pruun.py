import os.path
import subprocess

from click.testing import CliRunner
from pruun.commands import pruun
from pruun.utils import get_dependency_names


def test_deployment_package():
    """
    Test parsing of installed packages, creation of .zip, and finally validate integrity of .zip.
    """
    runner = CliRunner()
    lambda_file_name = "handler.py"
    package_name = "deployment_package.zip"

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

    cmd = f"unzip -l {package_name} {lambda_file_name}*"
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=True,
        check=True,
    )  # check .zip for lambda handler file
