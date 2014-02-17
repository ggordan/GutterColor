from os.path import join, dirname, realpath, isfile, exists
import GutterColor.settings as settings
from os import system, remove, makedirs
from GutterColor.line import Line
from sublime import Region
import re
from threading import Thread
import sublime
import shutil

class File(Thread):
  """Represents a file identified by the unique view buffer id"""

  def __init__(self, view, action = 'initialize'):
    """Initialize the File with a view"""
    Thread.__init__(self)
    self.view = view # sublime.View
    self.action = action
    self.id = self.view.buffer_id()


  def run(self):
    if self.action == 'initialize':
      self.initialize()
    elif self.action == 'update':
      self.update()


  def initialize(self):
    """Initialize the file by:
      * creating the icon directory,
      * writing all the identified colours in the file cache_path,
      * adding regions for all the found colours
    """

    # Create the icon directory if it doesn't already exist
    if not exists(self.icon_path()): makedirs(self.icon_path())

    # Return a list of all the line regions in the current file
    line_regions = self.view.lines(Region(0, self.view.size()))

    # Open the cache document
    file = open(self.cache_path(), 'w+')

    for line_number, region in enumerate(line_regions):

      line = Line(self.view, line_number, region, self.id)
      if line.has_color():
        line.add_region()
        file.write(line.formatted_line())


  def update(self):
    """Initialize the file by:
      * creating the icon directory,
      * writing all the identified colours in the file cache_path,
      * adding regions for all the found colours
    """

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
