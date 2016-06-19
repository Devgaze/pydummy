#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convenience wrapper for running pydummy directly from source tree."""

import sys
from pydummy.__main__ import main

if __name__ == '__main__':
    main(sys.argv[1:])