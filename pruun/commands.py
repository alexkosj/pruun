import click

from .utils import create_deployment_package, get_dependency_dirs, get_dependency_names


@click.group()
def pruun():
    pass


@pruun.command()
@click.argument(
    "handler_paths",
    nargs=-1,
    type=click.Path(exists=True),
)
@click.option(
    "--package-file",
    type=click.Path(),
    default="deployment_package.zip",
    help="Desired filename of deployment .zip file.",
)
def package(handler_paths, package_file):
    """
    Creates deployment package .zip file in current directory.

    handler_paths: Name(s) of Lambda handler file(s)/dir(s).
    Trailing slash for a directory path is optional.

    package-file (optional): Desired filename of deployment .zip file.
    Defaults to "deployment_package.zip".
    """
    depen_names = get_dependency_names()
    depen_dirs = get_dependency_dirs(depen_names)
    create_deployment_package(handler_paths, package_file, depen_dirs)
    click.echo("Finit!")
