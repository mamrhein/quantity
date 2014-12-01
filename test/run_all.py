#!/usr/bin/env python

import os, sys
from os.path import abspath, dirname
import unittest

packageDir = dirname(dirname(abspath(__file__)))
topDir = dirname(packageDir)
sys.path = [topDir] + sys.path

suite = unittest.defaultTestLoader.discover(packageDir, top_level_dir=topDir)
runner = unittest.TextTestRunner()
runner.run(suite)
