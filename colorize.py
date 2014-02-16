from os.path import join, dirname, realpath, isfile
from os import system, remove
from sublime import HIDDEN, PERSISTENT

class Colorize():

  def __init__(self, view, line_number, region, matched_line):
    self.view = view
    self.region = region
    self.line_number = line_number
    self.raw_color = matched_line.group(0)[1:]
    self.create_icon()
    self.add_region()

  def add(self):
    self.add_region()

  def destroy(self):
    self.erase_region()
    remove(self.icon_path())

  def color(self):
    if len(self.raw_color[1:]) is 3:
      return "%s%s" % [self.raw_color, self.raw_color[1:]]
    else:
      return "%s" % self.raw_color

  def create_icon(self):
    script = "convert -units PixelsPerCentimeter -channel RGBA -type TrueColorMatte -channel RGBA -size 16x16 -alpha transparent xc: -fill '#%s' -draw 'circle 7,7 8,10' png32:%s" % (self.color(), self.icon_path())
    if not isfile(self.icon_path()):
      system(script)

  def data(self):
    return {
      "key": "mark_%s" % self.line_number,
      "region": self.region
    }

  def icon_path(self):
    return join(dirname(realpath(__file__)), 'icons', '%s.png' % self.color())

  def relative_icon_path(self):
    return "Packages/GutterColor/icons/%s.png" % self.color()

  def erase_region(self):
    self.view.erase_regions("mark_%s" % self.line_number)

  # Add the icon to the current line
  def add_region(self):
    self.view.add_regions(
      "gcolor_%s" % [self.line_number],
      [self.region],
      "gutter_color",
      self.relative_icon_path(),
      HIDDEN | PERSISTENT
    )





