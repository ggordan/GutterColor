from sublime import Region
from threading import Thread
from .line import Line

class File():
  """ A File corresponds to one sublime.View """

  def __init__(self, view, action = 'initialize'):
    self.view = view # sublime.View
    self.id   = self.view.buffer_id()
    self.action = action
    self.scan()

  def scan(self):
    """Scan the file for colours and add/remove regions appropriately"""

    # Return a list of all the line regions in the current file
    if self.action == 'update':
      regions = [self.view.line(s) for s in self.view.sel()]
    else:
      regions = self.view.lines(Region(0, self.view.size()))

    for region in regions:
      line = Line(self.view, region, self.id)
      if line.has_color():
        line.add_region()
      else:
        try:
          self.view.erase_regions("gutter_color_%s" % region.a)
        except:
          pass
