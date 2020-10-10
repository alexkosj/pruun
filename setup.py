import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


setup(
    name="pruun",
    version="0.4.0",
    author="Alex Ko",
    author_email="alexkosj@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Pruun is a CL utility for easily creating AWS lambda deployment packages within Python virtualenvs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexkosj/pruun",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        pruun=pruun.commands:pruun
    """,
)
