from setuptools import setup

setup(
    name='pyack',
    version='0.1',
    py_modules=['pyack'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pyack=pyack:pyack
    ''',
)
