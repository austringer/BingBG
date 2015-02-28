#-*- encoding: utf-8 -*-

import os
import platform
import re
import sys
try:
  import configparser
  from urllib.request import urlopen
  from urllib.error import HTTPError
except ImportError:
  import ConfigParser as configparser
  from urllib2 import urlopen
  from urllib2 import HTTPError

from utils import *
from setwallpaper import *


def getConfig(config_path):

  config = configparser.ConfigParser()
  with open(config_path, 'r') as config_file:
    config.readfp(config_file)
  return config
global_config = getConfig(getThisFileDirectory() + os.sep + 'config.ini')


def getSettings(config, section, option):
  setting_string = config.get(section, option)
  settings = setting_string.split(',')
  settings = [s.strip() for s in settings]
  return settings


def getLanguageCultureFromConfig():
  return getSettings(global_config, 'source', 'language_culture')


def getResolutionFromConfig():
  return getSettings(global_config, 'source', 'resolution')


def getImageRootDirectoryFromConfig():
  directory = global_config.get('storage', 'directory')
  if not os.path.isabs(directory):
    directory = os.path.abspath(getThisFileDirectory() + os.sep + directory)
  if not os.path.exists(directory):
    os.makedirs(directory)
  elif not os.path.isdir(directory):
    print('%s already exists and is not a directory.' % directory)
    sys.exit()
  return directory


def getBingUrl(language_culture):
  bing_url = 'http://global.bing.com/?setmkt=%s' % language_culture
  print(bing_url)
  return bing_url


def getBingPage(bing_url):
  try:
    page = urlopen(bing_url).read()
  except HTTPError as e:
    page = e.read()
    print(page)
  return page


def getBingImageUrl(page, resolution):
  attr_pos = page.find(b'g_img=')
  if attr_pos != -1:
    attr_begin  = page.find(b'\'', attr_pos)
    attr_end    = page.find(b'\'', attr_begin + 1)
    image_url = page[attr_begin + 1: attr_end]

    if type(image_url) is not str:
      image_url = image_url.decode('utf-8')

    if not image_url.startswith('http'):
      image_url = 'http://global.bing.com' + image_url

    # replace resolution in url with target resolution
    image_url = re.sub(r'(?<=_)\d+x\d+(?=\.)', resolution, image_url)

    print(image_url)
    return image_url

  else:
    return ''


def needToBeUpdate(directory):
  latest_file = getLatestFile(directory)
  if latest_file == '':
    return True

  latest_modified = os.path.basename(latest_file)[:10]
  return latest_modified != getUTCDate()


def getImageDirectory(resolution, language_culture):
  root = getImageRootDirectoryFromConfig()
  image_directory = root + os.sep + resolution + os.sep + language_culture
  return image_directory

def getImageDirectoryAndName(image_url):
  pattern = re.compile(r'https?:\/\/.*\/(?P<name>[A-Za-z0-9-]+)_(?P<language_culture>[A-Za-z-]+)\d+_(?P<resolution>\d+x\d+)\.(?P<extension>[A-Za-z0-9]+)$')

  match = pattern.match(image_url)
  if match:
    name              = match.group('name')
    language_culture  = match.group('language_culture')
    resolution        = match.group('resolution')
    extension         = match.group('extension')

    image_directory = getImageDirectory(resolution, language_culture)
    image_name = '%s_%s.%s' % (getUTCDate(), name, extension)
    return image_directory, image_name

  else:
    print('Failed to parse image url.\n%s' % image_url)
    return '', ''


def generateBingImageTasks(language_culture, resolution):
  tasks = {}
  for lc in language_culture:
    bing_url  = getBingUrl(lc)
    bing_bage = getBingPage(bing_url)
    for rs in resolution:
      image_url = getBingImageUrl(bing_bage, rs)
      if image_url == '':
        continue

      image_directory, image_name = getImageDirectoryAndName(image_url)
      if image_directory == '' or image_name == '':
        continue

      if not os.path.exists(image_directory):
        os.makedirs(image_directory)

      if needToBeUpdate(image_directory):
        tasks[image_url] = image_directory + os.sep + image_name
  return tasks


def downloadBingImage(image_url, image_path):
  print('Downloading from %s to %s.' % (image_url, image_path))

  response = urlopen(image_url)
  with open(image_path, 'wb') as image_file:
    image_file.write(response.read())

  return image_path


# TODO
def windowsHardLinkAvailable():
  # see docs.python.org/3.2/library/os.html
  # os.link added Windows support in version 3.2
  current_version = platform.python_version()
  current_version_tuple = utils.getVersionTuple(current_version)
  least_version_tuple = current_version('3.2')
  return current_version_tuple >= (3, 2)


def getImageToBeWallpaper():
  resolution = global_config.get('wallpaper', 'resolution')
  language_culture = global_config.get('wallpaper', 'language_culture').upper()
  directory = getImageDirectory(resolution, language_culture)
  if not os.path.isdir(directory):
    print('Failed to find valid image directory. Check your configuration.')
    return ''

  latest_image = getLatestFile(directory)
  return latest_image


if __name__ == '__main__':
  language_culture = getLanguageCultureFromConfig()
  resolution = getResolutionFromConfig()
  tasks = generateBingImageTasks(language_culture, resolution)
  for url, path in tasks.items():
    downloadBingImage(url, path)

  image = getImageToBeWallpaper()
  if image != '':
    setWallpaper(image)