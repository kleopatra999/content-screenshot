# content-screenshot
Convert html and svg to png using the Blink-based rendering engine inside Chromium.

```
usage: contentScreenshot.py [-h] [--content-shell CONTENTSHELL]
                            [--flags FLAGS] [--width WIDTH] [--height HEIGHT]
                            [--no-svg-mode NOSVGMODE]
                            input output
```

# Examples

Convert [example.html](https://github.com/progers/content-screenshot/blob/master/example/example.html) to a png image:
```
$ ./contentScreenshot.py example/example.html html.png --width=245 --height=300
```
![example.html as an image](/example/htmlOutput.png)

ContentScreenshot can also be used as a modern svg->png converter. Lets convert [octocat.svg](https://github.com/progers/content-screenshot/blob/master/example/octocat.svg):
```
$ ./contentScreenshot.py example/octocat.svg svg.png --width=200
```
![example.html as an image](/example/svgOutput.png)
