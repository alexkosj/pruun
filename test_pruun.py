import os.path
import subprocess

from click.testing import CliRunner
from pruun import pruun


def test_deployment_package_creation():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("handler.py", "w") as f:  # create dummy lambda handler file
            pass

            result = runner.invoke(pruun, ["handler.py"])

            # check for no exceptions
            assert result.exit_code == 0

            # check for existence of .zip file
            assert os.path.isfile("deployment_package.zip") == True

            # validate zip contents
            test_unzip = subprocess.check_output(
                "unzip -t deployment_package.zip",
                stderr=subprocess.STDOUT,
                shell=True,
                universal_newlines=True,
            )
            assert "click/" in test_unzip

            f.close()
