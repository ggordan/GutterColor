from os.path import join, dirname, realpath, isfile
from os import system, remove
from sublime import HIDDEN, PERSISTENT, load_settings, cache_path
import subprocess
import re

class Line:

  HEX_REGEXP = '#((?:[0-9a-fA-F]{3}){1,2})'
  RGB_REGEXP = 'rgb\((\s*\d{1,3}\s*),(\s*\d{1,3}\s*),(\s*\d{1,3}\s*)?\)'

  def __init__(self, view, region, file_id):
    self.view     = view
    self.region   = region
    self.file_id  = file_id
    self.settings = load_settings("GutterColor.sublime-settings")
    self.text     = self.view.substr(self.region)

  def has_color(self):
    """Returns True/False depending on whether the line has a color in it"""
    return True if self.color() else False

  def color(self):
    """Returns the color in the line, if any."""
    return self.hex_color() if self.hex_color() else self.rgb_color()

  def hex_color(self):
    """Returns the color in the line, if any hex is found."""
    matches = re.search(Line.HEX_REGEXP, self.text)
    if matches:
      color = matches.group(1)
      if len(color) == 3:
        return "%s%s%s%s%s%s" % (
          color[0],
          color[0],
          color[1],
          color[1],
          color[2],
          color[2])
      else:
        return color

  def rgb_color(self):
    """Returns the color in the line, if any rgb is found."""
    matches = re.search(Line.RGB_REGEXP, self.text)
    if matches:
      try:
        r = int(matches.group(1), 10)
        g = int(matches.group(2), 10)
        b = int(matches.group(3), 10)
        return "%02x%02x%02x" % (r, g, b)
      except TypeError:
        pass

  def icon_path(self):
    """Returns the absolute path to the icons"""
    return join(cache_path(), 'GutterColor', '%s.png' % self.color())

  def relative_icon_path(self):
    """The relative location of the color icon"""
    return "Cache/GutterColor/%s.png" % (self.color())

  def add_region(self):
    """Add the icon to the gutter"""
    self.create_icon()
    self.view.add_regions(
      "gutter_color_%s" % self.region.a,
      [self.region],
      "gutter_color",
      self.relative_icon_path(),
      HIDDEN | PERSISTENT
    )

  def erase_region(self):
    """Remove icon from the gutter"""
    self.view.erase_regions("gutter_color_%s" % self.region.a)

  def create_icon(self):
    """Create the color icon using ImageMagick convert"""
    script = "%s -units PixelsPerCentimeter -type TrueColorMatte -channel RGBA " \
      "-size 32x32 -alpha transparent xc:none " \
      "-fill \"#%s\" -draw \"circle 15,16 8,10\" png32:\"%s\"" % \
      (self.settings.get("convert_path"), self.color(), self.icon_path())
    if not isfile(self.icon_path()):
        pr = subprocess.Popen(script,
          shell = True,
          stdout = subprocess.PIPE,
          stderr = subprocess.PIPE,
          stdin = subprocess.PIPE)
        (result, error) = pr.communicate()
