#!/usr/bin/env python

# chromium-content-screenshot.py [input_file] [output_file]
# Reads [input_file] as it would be renderered by chromium and writes the
# resulting png to [output_file].

import subprocess
import argparse
import platform
import subprocess
import os
import zipfile

def unzip(zipFile, outDir):
    with zipfile.ZipFile(zipFile, "r") as z:
        z.extractall(outDir)

def prebuiltContentShellBinary():
    system = platform.system()
    if (system == 'Darwin'):
        if (not os.path.isdir("contentShellBinaries/mac")):
            if (os.path.exists("contentShellBinaries/mac.zip")):
                unzip("contentShellBinaries/mac.zip", "contentShellBinaries/mac")
        macContentShell = "contentShellBinaries/mac/Content Shell.app/Contents/MacOS/Content Shell"
        if (os.path.exists(macContentShell)):
            return macContentShell
    #elif (system == 'Windows'):
    #    TODO: Build this.
    #elif (system == 'Linux'):
    #    if (platform.architecture()[0] == '32bit'):
    #        TODO: Build this.
    #    else:
    #        TODO: Build this.
    raise "A prebuilt content shell binary was not found for your platform. If you have a chromium checkout, you may specify your own content shell binary using --contentShell"

def dumpPng(contentShell, input, output, flags):
    print contentShell
    print flags
    print [contentShell,
                          "--run-layout-test",
                          "--enable-font-antialiasing",
                          flags,
                          # The single quote is a separator (see: layout_test_browser_main.cc)
                          input + "'--pixel-test"
                         ]
    p = subprocess.Popen([contentShell,
                          "--run-layout-test",
                          "--enable-font-antialiasing",
                          flags,
                          # The single quote is a separator (see: layout_test_browser_main.cc)
                          input + "'--pixel-test"
                         ],
                         shell = False,
                         stdout = subprocess.PIPE)
    result = p.stdout.read()
    PNG_START = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    PNG_END = b"\x49\x45\x4E\x44\xAE\x42\x60\x82"
    start = result.index(PNG_START)
    end = result.rindex(PNG_END) + 8
    with open(output, 'wb') as outputFile:
        outputFile.write(result[start:end])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='chromium-content-screenshot: command line tool for converting html/svg to png')
    parser.add_argument("input", help="input (html file, svg file, or url")
    parser.add_argument("output", help="output png result file")
    parser.add_argument("contentShell", help="content shell binary")
    parser.add_argument("--flags", help="additional flags to pass to content shell")
    parser.add_argument("--width", help="width of rendering (px)", type=int)
    parser.add_argument("--height", help="height of rendering (px)", type=int)
    args = parser.parse_args()

    flags = ""
    if (args.flags):
        flags = args.flags

    width = args.width if args.width else 800
    height = args.height if args.height else 600
    if ("content-shell-host-window-size" not in flags):
        size = "--content-shell-host-window-size=" + str(width) + "x" + str(height)
        flags = flags + " " + size

    dumpPng(args.contentShell, args.input, args.output, flags)