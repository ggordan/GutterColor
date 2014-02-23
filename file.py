from sublime import Region, version
from threading import Thread

# True if Sublime Text 3
ST3 = (int(version()) >= 3000)

if ST3: from .line import Line
else: from line import Line

class File(Thread):
  """ A File corresponds to one sublime.View """

  def __init__(self, view, action = 'initialize'):
    Thread.__init__(self)    
    self.view   = view # sublime.View
    self.id     = self.view.buffer_id()
    self.action = action
    if ST3 or action == 'update':
    	self.scan()

  def run(self):
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


