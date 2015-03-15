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

def prebuiltContentShellBinary(system, rev, binary):
    binaryRoot = "binaries" + "/" + rev + "." + system
    binaryPath = binaryRoot + "/" + binary
    zipPath = binaryRoot + ".zip"
    if (not os.path.exists(binaryPath)):
        if (os.path.exists(zipPath)):
            subprocess.call(["unzip", zipPath, "-d", binaryRoot], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (not os.path.exists(binaryPath)):
        raise Exception("A prebuilt content shell binary was not found for your platform. If you have a chromium checkout, you may specify your own content shell binary using --contentShell")
    return binaryPath

def contentShellBinary(contentShell):
    if (contentShell and os.path.exists(contentShell)):
        return contentShell
    system = platform.system()
    if (system == 'Darwin'):
        return prebuiltContentShellBinary("mac", "72cff265974701c8e6453e8b47a91d03053ea140", "Content Shell.app/Contents/MacOS/Content Shell")
    elif (system == 'Linux'):
        if (platform.architecture()[0] == '64bit'):
            return prebuiltContentShellBinary("linux64", "72cff265974701c8e6453e8b47a91d03053ea140", "content_shell")
    #elif (system == 'Windows'):
    #    TODO: Build this.
    raise Exception("A prebuilt content shell binary was not found for your platform. If you have a chromium checkout, you may specify your own content shell binary using --contentShell")

def dumpPng(contentShell, input, output, flags):
    if (not os.path.exists(input)):
        raise Exception("Input file not found")
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
    try:
        start = result.index(PNG_START)
        end = result.rindex(PNG_END) + 8
    except ValueError:
        raise Exception("Content shell did not output a valid png")
    with open(output, 'wb') as outputFile:
        outputFile.write(result[start:end])
        print "Done"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='chromium-content-screenshot: command line tool for converting html/svg to png')
    parser.add_argument("input", help="input (html file, svg file, or url")
    parser.add_argument("output", help="output png result file")
    parser.add_argument("--contentShell", help="content shell binary")
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

    dumpPng(contentShellBinary(args.contentShell), args.input, args.output, flags)