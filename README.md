[![Build Status](https://travis-ci.com/antimaLinux/kickscraper.svg?branch=develop)](https://travis-ci.com/antimaLinux/kickscraper)
# Kickscraper

Kickscraper is a tool to extract players scores from kickest platform.

## development

Setup a `venv`:

```console
python3 -m venv venv
```

Activate it:

```console
source venv/bin/activate
```

Install the package in editable mode:

```console
pip install -e .
```

## usage

Download data for the last games per player in JSONL format:

```console
kickeststats-download-data /tmp/players.jsonl
```

**NOTE:** requires Chrome installed.
