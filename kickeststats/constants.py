"""Contants for the kickeststats."""
import os
import pkg_resources
from kickeststats.exceptions import EnvVariableNotSet

CHROMEDRIVER_EXECUTABLE_PATH = os.environ.get(
    "CHROMEDRIVER_EXECUTABLE_PATH",
    pkg_resources.resource_filename(
        "kickeststats", "resources/drivers/chromedriver"
    )
)

if not CHROMEDRIVER_EXECUTABLE_PATH:
    raise EnvVariableNotSet("CHROMEDRIVER_EXECUTABLE_PATH")

KICKEST_URL = (
    "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?iframe=yes"
)
