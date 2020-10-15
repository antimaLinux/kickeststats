import io
import re

from setuptools import setup

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('kickeststats/__init__.py', encoding='utf_8_sig').read()
).group(1)

setup(
    name='kickeststats',
    version=__version__,
    author='Riccardo Vilardi, Matteo Manica',
    packages=['kickeststats'],
    long_description=open('README.md').read(),
    package_data={
        'kickeststats': [
            'py.typed',
            'resources/tests/players.jsonl'
        ]
    },
    install_requires=['pandas==1.1.2']
)
