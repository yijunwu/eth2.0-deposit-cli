from setuptools import find_packages, setup

"""
THIS IS A STUB FOR RUNNING THE APP
"""

setup(
    name="staking-deposit-cli",
    version='1.2.0',
    py_modules=["staking-deposit-cli"],
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires=">=3.7,<4",
)
