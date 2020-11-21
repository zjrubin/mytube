#!/usr/bin/env python3
import os

import yaml

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "mytube_config.yml")


def main():
    with open(CONFIG_FILE, "r") as infile:
        config = yaml.safe_load(infile)

    # print(config)


if __name__ == "__main__":
    main()
