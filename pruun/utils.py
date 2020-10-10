import os
import subprocess
from collections import defaultdict
from typing import Dict, List

import click

CMD_LINE_TIMEOUT = 10


def get_dependency_names() -> List[str]:
    """
    Returns list of installed package names, stripped of version tags.
    """
    pip_freeze_cmd_output = subprocess.check_output(
        "pip freeze --exclude-editable",
        stderr=subprocess.STDOUT,
        shell=True,
        timeout=CMD_LINE_TIMEOUT,
        universal_newlines=True,
    )
    depens = pip_freeze_cmd_output.split("\n")

    # strip off version tags, e.g. 'nodeenv==1.4.0' -> 'nodeenv'
    return [depen[: depen.index("=")] for depen in depens if depen]


def get_dependency_dirs(depen_names: List[str]) -> Dict[str, list]:
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


def create_deployment_package(
    handler_paths: str, package_file: str, depen_dirs: Dict[str, list]
):
    """
    Create .zip file containing lambda handler file and dependencies.
    """
    cwd = os.getcwd()
    package_file_path = os.path.join(cwd, package_file)
    exclusions = "-x .git/* */__pycache__/* *.pyc"

    click.echo("Creating deployment package...")
    for location, depen in depen_dirs.items():
        cmd = f'zip -r {package_file_path} {"* ".join(depen)}* {exclusions}'
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            cwd=location,
            shell=True,
            timeout=CMD_LINE_TIMEOUT,
            check=True,
        )

    cmd = f'zip -gr {package_file_path} {" ".join(handler_paths)} {exclusions}'
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        shell=True,
        timeout=CMD_LINE_TIMEOUT,
        check=True,
    )
