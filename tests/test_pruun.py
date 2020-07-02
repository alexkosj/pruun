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
