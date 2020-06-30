from setuptools import setup

setup(
    name="pruun",
    version="0.1",
    py_modules=["pruun"],
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        pruun=pruun:pruun
    """,
)
