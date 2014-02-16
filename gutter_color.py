from GutterColor.colorize import Colorize
from threading import Thread
from sublime_plugin import EventListener
from sublime import Region
import re

class GutterColorEventListener(EventListener):

  # TODO: This properly.
  def scan(self, view, action = 'add'):
    # Return a list of all the lines in the current view
    lines = view.lines(Region(0, view.size()))

    # Iterate through the lines
    for line_number, region in enumerate(lines):
      matched_line = re.search("#(?:[0-9a-fA-F]{3}){1,2}", view.substr(region))
      if matched_line:
        color = Colorize(view, line_number, region, matched_line)
        if action == 'add':
          color.add()
        else:
          color.destroy()
      else:
        view.erase_regions("gcolor_%s" % line_number)

  # Show the colours when the file is loaded
  def on_load_async(self, view):
    Thread(target = self.scan, args = [view, 'add']).start()

  def on_pre_save_async(self, view):
    Thread(target = self.scan, args = [view, 'add']).start()

  def on_close(self, view):
    Thread(target = self.scan, args = [view, 'destroy']).start()
