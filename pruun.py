import os.path
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List

import click

CMD_LINE_TIMEOUT = 10


@click.command()
@click.argument(
    "handler_file_path", type=click.Path(exists=True),
)
@click.option(
    "--package_file",
    type=click.Path(),
    default="deployment_package.zip",
    help="Desired filename of deployment .zip file.",
)
def pruun(handler_file_path, package_file):
    """
    Creates deployment package .zip file from installed pip packages.
    """
    depen_names = _get_dependency_names()
    depen_dirs = _get_dependency_dirs(depen_names)
    _create_deployment_package(package_file, depen_dirs)


def _get_dependency_names() -> List[str]:
    """
    Returns list of installed package names, stripped of version tags.
    """
    pip_freeze_cmd_output = subprocess.check_output(
        "pip freeze",
        stderr=subprocess.STDOUT,
        shell=True,
        timeout=CMD_LINE_TIMEOUT,
        universal_newlines=True,
    )
    depens = pip_freeze_cmd_output.split("\n")

    # strip off version tags, e.g. 'nodeenv==1.4.0' -> 'nodeenv'
    return [depen[: depen.index("=")] for depen in depens if depen]


def _get_dependency_dirs(depen_names: List[str]) -> Dict[str, list]:
    """
    Map package names to their location.
    """
    dirs = defaultdict(list)
    with click.progressbar(
        depen_names, label="Locating all installed packages..."
    ) as work:
        for name in work:
            # removes 'Location: ' prefix, e.g. 'Location: /home/user/.virtualenvs/pruun/lib/python3.7/site-packages' -> ' /home/user/.virtualenvs/pruun/lib/python3.7/site-packages'
            cmd = f'pip show {name} | grep "Location:" | cut -d ":" -f2'
            pip_show_cmd_output = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                shell=True,
                timeout=CMD_LINE_TIMEOUT,
                universal_newlines=True,
            ).strip()
            underscored_name = name.replace("-", "_").strip()
            dirs[pip_show_cmd_output].append(underscored_name)
        return dirs


def _create_deployment_package(package_file: str, depen_dirs: Dict[str, list]):
    """
    Create .zip file and move to project root dir.
    """
    project_dir = subprocess.check_output(
        "pwd",
        stderr=subprocess.STDOUT,
        shell=True,
        timeout=CMD_LINE_TIMEOUT,
        universal_newlines=True,
    )

    for location, depen in depen_dirs.items():
        cmd = f'zip -r {package_file} {" ".join(depen)}'
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            cwd=location,
            shell=True,
            timeout=CMD_LINE_TIMEOUT,
            check=True,
        )
        subprocess.run(
            f"mv {package_file} {project_dir}",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            cwd=location,
            shell=True,
            timeout=CMD_LINE_TIMEOUT,
            check=True,
        )
    click.echo("Finit!")


if __name__ == "__main__":
    pruun()
