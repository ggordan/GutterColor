from os.path import join, dirname, realpath, isfile
from os import system, remove
import GutterColor.settings as settings
from sublime import HIDDEN, PERSISTENT, load_settings
import re

class Line:

  def __init__(self, view, line_number, region, file_id):
    self.view     = view
    self.region   = region
    self.file_id  = file_id
    self.line_number = line_number
    self.settings = load_settings("GutterColor.sublime-settings")



  def has_color(self):
    """Returns True/False depending on whether the line has a color in it"""
    return True if self.color() else False


  def color(self):
    """Returns the color in the line, if any."""
    color = re.search("#(?:[0-9a-fA-F]{3}){1,2}", self.view.substr(self.region))
    if color:
      color = color.group(0)
      if len(color[1:]) is 3:
        return "%s%s" % (color[1:], color[1:])
      else:
        return "%s" % color[1:]


  def icon_path(self):
    """Returns the absolute path to the icons"""
    return join(settings.ICON_PATH, str(self.file_id), '%s.png' % self.color())


  def relative_icon_path(self):
    """The relative location of the color icon"""
    return "Packages/GutterColor/icons/%s/%s.png" % (str(self.file_id), self.color())


  def add_region(self):
    """Add the icon to the gutter"""
    self.create_icon()
    self.view.add_regions(
      "gutter_color_%s" % self.line_number,
      [self.region],
      "gutter_color",
      self.relative_icon_path(),
      HIDDEN
    )


  def erase_region(self):
    """Remove icon from the gutter"""
    self.view.erase_regions("gutter_color_%s" % self.line_number)


  def create_icon(self):
    """Create the color icon using ImageMagick convert"""

    script = "%s -units PixelsPerCentimeter -type TrueColorMatte -channel RGBA -size 16x16 -alpha transparent xc: -fill '#%s' -draw 'circle 7,7 8,10' png32:\"%s\"" % (self.settings.get("convert_path"), self.color(), self.icon_path())
    if not isfile(self.icon_path()):
      system(script)


  def formatted_line(self):
    """Returns the formatted line which will be stored in the cache"""
    return "%s|%s\n" % (self.line_number, self.color())
