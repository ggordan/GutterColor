from os.path import join, dirname, realpath, isfile
from os import system, remove
import GutterColor.settings as settings
from sublime import HIDDEN, PERSISTENT
import re

class Line:

  def __init__(self, view, line_number, region, file_id):
    self.view     = view
    self.region   = region
    self.file_id  = file_id
    self.line_number = line_number

  # Returns a boolean value depending on whether the current line has a color
  # inside it
  # TODO: If the file is SASS/LESS, check if the color is matched by a variable
  # also add support for RGB(a) and HSL colors
  def has_color(self):
    if self.color():
      return True
    else:
      return False


  # Return the color found in the line, if any
  def color(self):
    color = re.search("#(?:[0-9a-fA-F]{3}){1,2}", self.view.substr(self.region))
    if color:
      color = color.group(0)
      if len(color[1:]) is 3:
        return "%s%s" % (color[1:], color[1:])
      else:
        return "%s" % color[1:]
    else:
      return False


  # Returns the absolute path to the icons
  def icon_path(self):
    return join(settings.ICON_PATH, str(self.file_id), '%s.png' % self.color())


  # The relative location of the color icon
  def relative_icon_path(self):
    return "Packages/GutterColor/icons/%s/%s.png" % (str(self.file_id), self.color())


  def add_region(self):
    self.create_icon()
    self.view.add_regions(
      "gutter_color_%s" % [self.line_number],
      [self.region],
      "gutter_color",
      self.relative_icon_path(),
      HIDDEN | PERSISTENT
    )


  def erase_region(self):
    print(self.view.get_regions("gutter_color_%s" % self.line_number))
    self.view.erase_regions("gutter_color_%s" % self.line_number)

  # Create the color icon using ImageMagick convert
  def create_icon(self):
    script = "convert -units PixelsPerCentimeter -channel RGBA -type TrueColorMatte -channel RGBA -size 16x16 -alpha transparent xc: -fill '#%s' -draw 'circle 7,7 8,10' png32:%s" % (self.color(), self.icon_path())
    if not isfile(self.icon_path()):
      system(script)


  # Returns the formatted line which will be stored in the cache
  def formatted_line(self):
    return "%s|%s\n" % (self.line_number, self.color())
