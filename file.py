from os.path import join, dirname, realpath, isfile, exists
import GutterColor.settings as settings
from os import system, remove, makedirs
from GutterColor.line import Line
from sublime import Region
import re
import threading
import sublime
import shutil

class File:
  """Represents a file identified by the unique view buffer id"""

  def __init__(self, view):
    """Initialize the File with a view"""

    # Store the unique ID of the file
    self.id = view.buffer_id()
    # The the sublime.View
    self.view = view


  def initialize(self):
    """Initialize the file by:
      * creating the icon directory,
      * writing all the identified colours in the file cache_path,
      * adding regions for all the found colours
    """

    # Create the icon directory if it doesn't already exist
    if not exists(self.icon_path()): makedirs(self.icon_path())

    # Return a list of all the lines in the current view
    lines = self.view.lines(Region(0, self.view.size()))
    # Open the document for writing
    file = open(self.cache_path(), 'w+')
    # Iterate through the lines
    for line_number, region in enumerate(lines):
      line = Line(self.view, line_number, region, self.id)
      if line.has_color():
        line.add_region()
        file.write(line.formatted_line())


  def update(self):
    file = open(self.cache_path(), 'r').readlines()
    existing_lines = []
    for line in file:
      obj = line.strip().split('|')
      existing_lines.append(obj[0])
    # Return a list of all the lines in the current view
    lines = self.view.lines(Region(0, self.view.size()))

    # Open the document for writing
    file = open(self.cache_path(), 'w+')
    # Iterate through the lines
    for line_number, region in enumerate(lines):
      line = Line(self.view, line_number, region, self.id)
      if line.has_color():
        line.add_region()
        file.write(line.formatted_line())
      else:
        self.view.erase_regions("gutter_color_%s" % line_number)


  def cache_path(self):
    """Returns the cache path of the file"""
    return join(settings.CACHE_PATH, str(self.id))


  def icon_path(self):
    """Returns the directory of the icons"""
    return join(settings.ICON_PATH, str(self.id))


  def close(self):
    """Clean up all the assets created by the current file"""
    try:
      shutil.rmtree(self.icon_path())
      remove(self.cache_path())
    except FileNotFoundError:
      pass
