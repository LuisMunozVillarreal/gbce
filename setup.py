"""Setuptools configuration."""


from setuptools import find_packages, setup

setup(
    name="gbce",
    packages=find_packages(exclude=["tests*"]),
    version="0.1",
    extras_require={
        "test": [
            "black==22.6.0",
            "flake8==3.8.4",
            "flake8-isort==4.0.0",
            "mypy==0.961",
            "pydocstyle==6.1.1",
            "pylint==2.7.2",
            "pytest-cov==2.11.1",
            "pytest-factoryboy==2.1.0",
            "pytest-mock==3.5.1",
            "pytest-xdist==2.2.0",
            "pytest==7.1.2",
            "toml==0.10.2",
        ],
        "dev": [
            "ipython==7.21.0",
            "ipdb==0.13.5",
        ],
    },
)
