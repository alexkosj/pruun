import click

from .utils import create_deployment_package, get_dependency_dirs, get_dependency_names


@click.group()
def pruun():
    pass


@pruun.command()
@click.argument(
    "handler_file", type=click.Path(exists=True),
)
@click.option(
    "--package-file",
    type=click.Path(),
    default="deployment_package.zip",
    help="Desired filename of deployment .zip file.",
)
def package(handler_file, package_file):
    """
    Creates deployment package .zip file in current directory.
    
    handler_file (str): Name of Lambda handler file. 
    Assumed to exist within current directory.

    package-file (str, optional): Desired filename of deployment .zip file. 
    Defaults to "deployment_package.zip".
    """
    depen_names = get_dependency_names()
    depen_dirs = get_dependency_dirs(depen_names)
    create_deployment_package(handler_file, package_file, depen_dirs)
    click.echo("Finit!")
