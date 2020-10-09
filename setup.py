import io
import re

from setuptools import setup

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('kickscraper/__init__.py', encoding='utf_8_sig').read()
).group(1)

setup(
    name='kickscraper',
    version=__version__,
    author='Riccardo Vilardi, Matteo Manica',
    packages=['kickscraper'],
    long_description=open('README.md').read(),
    package_data={'kickscraper': ['py.typed']},
    install_requires=['pandas==1.1.2']
)
