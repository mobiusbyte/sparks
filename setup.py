from setuptools import setup, find_packages

setup(
    name="sparks",
    version="0.1.0",
    author="Jill San Luis",
    license="MIT",
    packages=find_packages(exclude=["test", "test.*"]),
    entry_points={"console_scripts": ["sparks=sparks.console.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
