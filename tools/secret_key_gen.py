#!/usr/bin/env python
import logging
from django.utils.crypto import get_random_string


logger = logging.getLogger(__name__)


def run():
    print("Creating new secret key")
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    secret = get_random_string(50, chars)
    print(secret)
    print("Done")


if __name__ == "__main__":
    run()
