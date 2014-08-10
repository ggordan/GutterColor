# Gutter Color

Gutter Color is a cross-platform Sublime Text plugin which displays a colored icon for all lines which contain a color.

![GutterColor](screenshot.png)

## Requirements

* [ImageMagick](http://www.imagemagick.org/)

## Configure

* Install ImageMagick
* Set the `convert_path` in `Preferences: Package Settings > GutterColor > Settings – User` to the location of the ImageMagick `convert` script:

```json
{
  "convert_path" : "/usr/local/bin/convert"
}
```
* For help with either, view [this blog post by Wes Bos](http://wesbos.com/css-gutter-color-sublime-text/)

## 100% Perfect Colors
Add the following to your SublimeText theme file:

```xml
<dict>
  <key>name</key>
  <string>GutterColor</string>
  <key>scope</key>
  <string>gutter_color</string>
  <key>settings</key>
  <dict>
    <key>foreground</key>
    <string>#ffffff</string>
  </dict>
</dict>
```

## TODO

* Add support for SASS/LESS variables
* Backport to ST2
* Handle conflicts with GitGutter/VCS Gutter

## Thanks
Thanks to all of the [contributors](https://github.com/ggordan/GutterColor/graphs/contributors) who continue to improve GutterColor!
