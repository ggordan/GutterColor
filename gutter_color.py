from GutterColor.colorize import Colorize
from GutterColor.file import File
from threading import Thread
from sublime_plugin import EventListener

class GutterColorEventListener(EventListener):

  # Show the colours when the file is loaded
  def on_load_async(self, view):
    File(view).initialize()
    # Thread(target = self.scan, args = [view, 'add']).start()

  def on_pre_save_async(self, view):
    File(view).update()

  def on_close(self, view):
    File(view).close()
