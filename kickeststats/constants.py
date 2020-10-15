import os
from kickeststats.exceptions import EnvVariableNotSet

CHROMEDRIVER_EXECUTABLE_PATH = os.environ.get("CHROMEDRIVER_EXECUTABLE_PATH")

if not CHROMEDRIVER_EXECUTABLE_PATH:
    raise EnvVariableNotSet("CHROMEDRIVER_EXECUTABLE_PATH")

KICKEST_URL = (
    "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?iframe=yes"
)
