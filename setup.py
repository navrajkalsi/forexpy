from setuptools import setup, find_packages

setup(
    name = "FxPy",
    version = "1.1.2",
    packages = find_packages(),
    install_requires = ["pycountry", "pynput", "requests", "beautifulsoup4", "keyboard", "pandas", "openpyxl", "argparse"],
    entry_points = {
        "console_scripts": [
            "fxpy = fxpy.start:main",
        ]
    },
    author = "Navraj Singh Kalsi",
    description = "ForexPy: A currency conversion tool that also scraps the web and gives the Forex Exchange rates from major services.",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://www.github.com/navrajkalsi/fxpy",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
