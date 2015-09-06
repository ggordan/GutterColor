from os.path import join, dirname, realpath, isfile
from sublime import HIDDEN, PERSISTENT, load_settings, cache_path
import subprocess, os, glob, re, platform

css3_names_to_hex = {'aliceblue': '#f0f8ff',
 'antiquewhite': '#faebd7',
 'aqua': '#00ffff',
 'aquamarine': '#7fffd4',
 'azure': '#f0ffff',
 'beige': '#f5f5dc',
 'bisque': '#ffe4c4',
 'black': '#000000',
 'blanchedalmond': '#ffebcd',
 'blue': '#0000ff',
 'blueviolet': '#8a2be2',
 'brown': '#a52a2a',
 'burlywood': '#deb887',
 'cadetblue': '#5f9ea0',
 'chartreuse': '#7fff00',
 'chocolate': '#d2691e',
 'coral': '#ff7f50',
 'cornflowerblue': '#6495ed',
 'cornsilk': '#fff8dc',
 'crimson': '#dc143c',
 'cyan': '#00ffff',
 'darkblue': '#00008b',
 'darkcyan': '#008b8b',
 'darkgoldenrod': '#b8860b',
 'darkgray': '#a9a9a9',
 'darkgrey': '#a9a9a9',
 'darkgreen': '#006400',
 'darkkhaki': '#bdb76b',
 'darkmagenta': '#8b008b',
 'darkolivegreen': '#556b2f',
 'darkorange': '#ff8c00',
 'darkorchid': '#9932cc',
 'darkred': '#8b0000',
 'darksalmon': '#e9967a',
 'darkseagreen': '#8fbc8f',
 'darkslateblue': '#483d8b',
 'darkslategray': '#2f4f4f',
 'darkslategrey': '#2f4f4f',
 'darkturquoise': '#00ced1',
 'darkviolet': '#9400d3',
 'deeppink': '#ff1493',
 'deepskyblue': '#00bfff',
 'dimgray': '#696969',
 'dimgrey': '#696969',
 'dodgerblue': '#1e90ff',
 'firebrick': '#b22222',
 'floralwhite': '#fffaf0',
 'forestgreen': '#228b22',
 'fuchsia': '#ff00ff',
 'gainsboro': '#dcdcdc',
 'ghostwhite': '#f8f8ff',
 'gold': '#ffd700',
 'goldenrod': '#daa520',
 'gray': '#808080',
 'grey': '#808080',
 'green': '#008000',
 'greenyellow': '#adff2f',
 'honeydew': '#f0fff0',
 'hotpink': '#ff69b4',
 'indianred': '#cd5c5c',
 'indigo': '#4b0082',
 'ivory': '#fffff0',
 'khaki': '#f0e68c',
 'lavender': '#e6e6fa',
 'lavenderblush': '#fff0f5',
 'lawngreen': '#7cfc00',
 'lemonchiffon': '#fffacd',
 'lightblue': '#add8e6',
 'lightcoral': '#f08080',
 'lightcyan': '#e0ffff',
 'lightgoldenrodyellow': '#fafad2',
 'lightgray': '#d3d3d3',
 'lightgrey': '#d3d3d3',
 'lightgreen': '#90ee90',
 'lightpink': '#ffb6c1',
 'lightsalmon': '#ffa07a',
 'lightseagreen': '#20b2aa',
 'lightskyblue': '#87cefa',
 'lightslategray': '#778899',
 'lightslategrey': '#778899',
 'lightsteelblue': '#b0c4de',
 'lightyellow': '#ffffe0',
 'lime': '#00ff00',
 'limegreen': '#32cd32',
 'linen': '#faf0e6',
 'magenta': '#ff00ff',
 'maroon': '#800000',
 'mediumaquamarine': '#66cdaa',
 'mediumblue': '#0000cd',
 'mediumorchid': '#ba55d3',
 'mediumpurple': '#9370d8',
 'mediumseagreen': '#3cb371',
 'mediumslateblue': '#7b68ee',
 'mediumspringgreen': '#00fa9a',
 'mediumturquoise': '#48d1cc',
 'mediumvioletred': '#c71585',
 'midnightblue': '#191970',
 'mintcream': '#f5fffa',
 'mistyrose': '#ffe4e1',
 'moccasin': '#ffe4b5',
 'navajowhite': '#ffdead',
 'navy': '#000080',
 'oldlace': '#fdf5e6',
 'olive': '#808000',
 'olivedrab': '#6b8e23',
 'orange': '#ffa500',
 'orangered': '#ff4500',
 'orchid': '#da70d6',
 'palegoldenrod': '#eee8aa',
 'palegreen': '#98fb98',
 'paleturquoise': '#afeeee',
 'palevioletred': '#d87093',
 'papayawhip': '#ffefd5',
 'peachpuff': '#ffdab9',
 'peru': '#cd853f',
 'pink': '#ffc0cb',
 'plum': '#dda0dd',
 'powderblue': '#b0e0e6',
 'purple': '#800080',
 'red': '#ff0000',
 'rosybrown': '#bc8f8f',
 'royalblue': '#4169e1',
 'saddlebrown': '#8b4513',
 'salmon': '#fa8072',
 'sandybrown': '#f4a460',
 'seagreen': '#2e8b57',
 'seashell': '#fff5ee',
 'sienna': '#a0522d',
 'silver': '#c0c0c0',
 'skyblue': '#87ceeb',
 'slateblue': '#6a5acd',
 'slategray': '#708090',
 'slategrey': '#708090',
 'snow': '#fffafa',
 'springgreen': '#00ff7f',
 'steelblue': '#4682b4',
 'tan': '#d2b48c',
 'teal': '#008080',
 'thistle': '#d8bfd8',
 'tomato': '#ff6347',
 'turquoise': '#40e0d0',
 'violet': '#ee82ee',
 'wheat': '#f5deb3',
 'white': '#ffffff',
 'whitesmoke': '#f5f5f5',
 'yellow': '#ffff00',
 'yellowgreen': '#9acd32'}

class Line:

  # A digit is one-three numbers, with an optional floating point part,
  # and maybe a % sign, and maybe surrounded by whitespace.
  DIGIT = '\s*\d{1,3}(\.\d*)?%?\s*'

  # Three digits is three digits, with commas between.
  THREE_DIGITS = DIGIT + ',' + DIGIT + ',' + DIGIT

  # Four digits is three digits (which we save for later),
  # and then a comma and then the fourth digit.
  FOUR_DIGITS = '(' + THREE_DIGITS + '),' + DIGIT

  HEX_REGEXP = '#((?:[0-9a-fA-F]{3}){1,2}(?![0-9a-fA-F]+))'
  RGB_REGEXP = 'rgb\(' + THREE_DIGITS + '\)'
  RGBA_REGEXP = 'rgba\(' + FOUR_DIGITS + '\)'
  HSL_REGEXP = 'hsl\(' + THREE_DIGITS + '\)'
  HSLA_REGEXP = 'hsla\(' + FOUR_DIGITS + '\)'
  WEB_COLORS_REGEX = ''
  WEB_COLORS = []

  def __init__(self, view, region, file_id):
    self.generate_webcolors()

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
    if self.web_color():
      return self.web_color()
    if self.hex_color():
      return self.hex_color()
    if self.rgb_color():
      return self.rgb_color()
    if self.rgba_color():
      return self.rgba_color()
    if self.hsl_color():
      return self.hsl_color()
    if self.hsla_color():
      return self.hsla_color()
    if not self.settings.get("custom_colors") == None:
      return self.custom_color()

  def generate_webcolors(self):
    """Generates a list of web color names."""
    self.WEB_COLORS = dict((name, color) for (name, color) in css3_names_to_hex.items())
    self.WEB_COLORS_REGEX = '((?<!\$)'+ '|(?<!\$)'.join(self.WEB_COLORS.keys()) +')'

  def web_color(self):
    """Returns the color in the line, if any CSS color name is found."""
    matches = re.search(self.WEB_COLORS_REGEX, self.text)
    if matches:
      return matches.group(0)

  def hex_color(self):
    """Returns the color in the line, if any hex is found."""
    matches = re.search(Line.HEX_REGEXP, self.text)
    if matches:
      return matches.group(0)

  def rgb_color(self):
    """Returns the color in the line, if any rgb is found."""
    matches = re.search(Line.RGB_REGEXP, self.text)
    if matches:
      return matches.group(0)

  def rgba_color(self):
    """Returns the color in the line, if any rgba is found."""
    matches = re.search(Line.RGBA_REGEXP, self.text)
    if matches:
      if self.transparency_settings()[0]:
        return matches.group(0)
      else:
        return 'rgb(' + matches.group(1) + ')'

  def hsl_color(self):
    """Returns the color in the line, if any hsl is found."""
    matches = re.search(Line.HSL_REGEXP, self.text)
    if matches:
      return matches.group(0)

  def hsla_color(self):
    """Returns the color in the line, if any hsla is found."""
    matches = re.search(Line.HSLA_REGEXP, self.text)
    if matches:
      if self.transparency_settings()[0]:
        return matches.group(0)
      else:
        return 'hsl(' + matches.group(1) + ')'

  def custom_color(self):
    """Returns the color in the line, if any user-defined is found."""
    user_colors = self.settings.get("custom_colors")
    for user_color in user_colors:
      matches = re.search(user_color["regex"], self.text)
      group_id = user_color["group_id"] if "group_id" in user_color else 0
      prefix = user_color["output_prefix"] if "output_prefix" in user_color else ""
      suffix = user_color["output_suffix"] if "output_suffix" in user_color else ""
      if matches:
        return prefix+matches.group(group_id)+suffix

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

  def transparency_settings(self):
    from .gutter_color import current_directory
    # transparency settings
    use_transparency = self.settings.get("use_transparency")
    if use_transparency == True:
      background_path = os.path.join(current_directory(True),"transparency_circle_mid.png")
    elif use_transparency in ("light", "mid"):
      background_path = os.path.join(current_directory(True),str("transparency_circle_"+use_transparency+".png"))
      print(background_path)
      use_transparency = True
    else:
      use_transparency = False
    return (use_transparency, background_path)

  def create_icon(self):
    paths = [
      self.settings.get("convert_path"),
      "/usr/bin/convert",
      "/usr/local/bin",
      "/usr/bin"
    ]

    if ( platform.system()=="Windows"):
      delimiter = ";"
      convert_name = "convert.exe"
    else:
      delimiter = ":"
      convert_name = "convert"

    paths.extend(glob.glob('/usr/local/Cellar/imagemagick/*/bin'))
    paths.extend(os.environ['PATH'].split(delimiter))

    convert_path = None
    for path in paths:
      if not path.endswith(convert_name):
        path = os.path.join(path,convert_name)
      if os.path.isfile(path) and os.access(path, os.X_OK):
        convert_path = path
        break

    (use_transparency, background_path) = self.transparency_settings()

    """Create the color icon using ImageMagick convert"""
    if not use_transparency:
      script = "\"%s\" -units PixelsPerCentimeter -type TrueColorMatte -channel RGBA " \
        "-size 32x32 -alpha transparent xc:none " \
        "-fill \"%s\" -draw \"circle 15,16 8,10\" png32:\"%s\"" % \
        (convert_path, self.color(), self.icon_path())
    else:
      script = "\"%s\" \"%s\" -type TrueColorMatte -channel RGBA " \
        "-fill \"%s\" -draw \"circle 15,16 8,10\" png32:\"%s\"" % \
        (convert_path, background_path, self.color(), self.icon_path())
    if not isfile(self.icon_path()):
        pr = subprocess.Popen(script,
          shell = True,
          stdout = subprocess.PIPE,
          stderr = subprocess.PIPE,
          stdin = subprocess.PIPE)
        (result, error) = pr.communicate()
