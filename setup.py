from setuptools import find_packages, setup

setup(
    name="pyVSSSReferee",
    packages=find_packages(include=['pyVSSSReferee']),
    version="0.1",
    description="Creates a network socket to communicate with the VSSS League referee",
    author="Project-Neon",
    license="GNU",
    install_requires=['protobuf==3.6.1'],
)
