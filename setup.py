import io
import re

from setuptools import setup

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open("kickeststats/__init__.py", encoding="utf_8_sig").read()
).group(1)

setup(
    name="kickeststats",
    version=__version__,
    author="Riccardo Vilardi, Matteo Manica",
    packages=["kickeststats"],
    long_description=open("README.md").read(),
    package_data={
        "kickeststats": [
            "py.typed",
            "resources/tests/players.jsonl",
            "resources/drivers/chromedriver"
        ]
    },
    install_requires=[
        "pandas==1.1.2", "loguru==0.5.3",
        "splinter==0.14.0", "black==19.10b0"
    ],
    scripts=["bin/kickeststats-download-data"]
)
