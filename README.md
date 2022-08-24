[![Build Status](https://travis-ci.com/antimaLinux/kickscraper.svg?branch=develop)](https://travis-ci.com/antimaLinux/kickscraper)
# Kickscraper

Kickscraper is a tool to extract players scores from kickest platform.

## requirements

The package is tested only with the following python versions:

- 3.7
- 3.8

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

Download data for player stats in the last game rounds in JSONL format:

```console
kickeststats-download-data /tmp/players.jsonl
```

**NOTE:** requires Chrome installed.
