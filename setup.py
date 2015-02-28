#-*- encoding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(
  console=['bingbg.py'],
  options={
    'py2exe':{
      'bundle_files': 2,
      'dist_dir': '.',
    }
  }
)