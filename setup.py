from setuptools import setup, find_packages

setup(
    name = "FxPy",
    version = "1.2.1",
    description = "ForexPy: A currency conversion tool that also scraps the web and gives the Forex Exchange rates from major services.",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    author = "Navraj Singh Kalsi",
    author_email = "navrajkalsi@icloud.com",
    url = "https://www.github.com/navrajkalsi/forexpy",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
    install_requires = [
        "pycountry",
        "requests",
        "beautifulsoup4",
        "keyboard",
        "pandas",
        "argparse",
        "importlib.metadata"
    ],
    entry_points = {
        "console_scripts": [
            "fxpy = fxpy.start:main",
        ]
    }
)
