from os.path import join, dirname, realpath, isfile, exists
import GutterColor.settings as settings
from os import system, remove, makedirs
from GutterColor.colorize import Colorize
from GutterColor.line import Line
from sublime import Region
import re
import shutil

# Represents a file identified by the unique view buffer id
class File:

  def __init__(self, view):
    self.view = view
    self.id = view.buffer_id()

    # The location of the file
    self.path = join(settings.CACHE_PATH, str(self.id))
    self.icon_dir = join(settings.ICON_PATH, str(self.id))

    # Create the icon directory
    if not exists(self.icon_dir):
      makedirs(self.icon_dir)


  # Once a file is opened create a new file in .cache/buffer_id to store the
  # color, line number, and region touple
  def initialize(self):
    # Return a list of all the lines in the current view
    lines = self.view.lines(Region(0, self.view.size()))
    # Open the document for writing
    file = open(self.path, 'w+')
    # Iterate through the lines
    for line_number, region in enumerate(lines):
      line = Line(self.view, line_number, region, self.id)
      if line.has_color():
        line.add_region()
        file.write(line.formatted_line())


  def update(self):
    file = open(self.path, 'r').readlines()
    existing_lines = []
    for line in file:
      obj = line.strip().split('|')
      existing_lines.append(obj[0])
    # Return a list of all the lines in the current view
    lines = self.view.lines(Region(0, self.view.size()))
    # Open the document for writing
    file = open(self.path, 'w+')
    # Iterate through the lines
    for line_number, region in enumerate(lines):
      line = Line(self.view, line_number, region, self.id)
      if line.has_color():
        line.add_region()
        file.write(line.formatted_line())
      else:
        line.erase_region()


  # Clean up all the assets created with the current file.
  # * Remove the cache file
  # * Remove the image icons
  def close(self):
    try:
      shutil.rmtree(self.icon_dir)
      remove(self.path)
    except FileNotFoundError:
      pass
