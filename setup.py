from setuptools import setup, find_packages

setup(
    name="spark",
    version="0.1.0",
    author="Jill San Luis",
    packages=find_packages(),
    entry_points={"console_scripts": ["spark=spark.console.cli:main"]},
)
