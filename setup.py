from setuptools import setup, find_packages

with open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

# Ugly! Duplicated from Pipfile
required = ["click", "jinja2", "pyyaml"]

extras = {"dev": ["black==19.3b0", "pre-commit", "pytest", "pytest-cov"]}

setup(
    name="Sparks",
    version="0.1.0",
    url="https://github.com/binaryart/sparks",
    project_urls={
        "Code": "https://github.com/binaryart/sparks",
        "Issue tracker": "https://github.com/binaryart/sparks/issues",
    },
    license="MIT",
    author="Jill San Luis",
    author_email="jill.devs@gmail.com",
    packages=find_packages(exclude=["test", "test.*"]),
    entry_points={"console_scripts": ["sparks=sparks.console.cli:main"]},
    description="A CLI tool that creates and updates project folders from "
    "templates to spark faster project bootstrapping.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    install_requires=required,
    extras_require=extras,
)
