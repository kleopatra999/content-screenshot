#!/usr/bin/env python

# content-screenshot.py input_file output_file
# Reads input_file as it would be renderered by Chromium and writes the
# resulting png to output_file.

import subprocess
import argparse
import platform
import subprocess
import os
import urllib
import base64

def htmlAsPng(contentShell, inputHtmlPath, flags, width, height):
    # Use a special flag for controlling the window size.
    SIZE_FLAG = "--content-shell-host-window-size"
    width = width if width else 800
    height = height if height else 600
    if (SIZE_FLAG not in flags):
        flags = flags + " " + SIZE_FLAG + "=" + str(width) + "x" + str(height)

    # Pixel results are enabled with the pixel-test "flag" after the input.
    # The single quote is a separator (see: layout_test_browser_main.cc).
    inputHtmlPath = inputHtmlPath + "'--pixel-test"

    rawResult = runContentShell(contentShell, inputHtmlPath, flags)

    PNG_START = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    PNG_END = b"\x49\x45\x4E\x44\xAE\x42\x60\x82"
    try:
        start = rawResult.index(PNG_START)
        end = rawResult.rindex(PNG_END) + 8
    except:
        raise Exception("Content shell did not output a valid png")
    return rawResult[start:end]

# Return the path to the svg-as-base64-png helper script which dumps a base64-
# encoded png file to the console.
def svgAsBase64PngHelperPath(input, width, height):
    dumpSvgPng = "svg-as-base64-png.html"
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    dumpSvgPngPath = scriptPath + "/" + dumpSvgPng
    if (not os.path.exists(dumpSvgPngPath)):
        raise Exception(dumpSvgPngPath + " was not found")
    if (os.path.exists(input)):
        input = "file://" + os.getcwd() + "/" + input
    size = ""
    if (width):
        size = size + "width=" + str(width)
    if (height):
        if (len(size) > 0):
            size = size + "&"
        size = size + "height=" + str(height)
    url = ""
    if (len(size) > 0):
        url = "&"
    url = url + "url=" + urllib.quote(input)
    return "file://" + dumpSvgPngPath + "?" + size + url

def svgAsPng(contentShell, inputSvgPath, flags, width, height):
    inputSvgPath = svgAsBase64PngHelperPath(inputSvgPath, width, height)

    rawResult = runContentShell(contentShell, inputSvgPath, flags)

    SVG_PNG_START = "SvgPngBase64Encoded->"
    SVG_PNG_END = "<-SvgPngBase64Encoded"
    try:
        start = rawResult.index(SVG_PNG_START) + len(SVG_PNG_START)
        end = rawResult.index(SVG_PNG_END)
        return base64.decodestring(rawResult[start:end])
    except:
        raise Exception("Content shell did not output a valid svg png")

def unpackPrebuiltContentShellBinary(system, rev, binary):
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    binaryRoot = scriptPath + "/bin/" + rev + "." + system
    binaryPath = binaryRoot + "/" + binary
    zipPath = binaryRoot + ".zip"
    if (not os.path.exists(binaryPath)):
        if (os.path.exists(zipPath)):
            subprocess.call(["unzip", zipPath, "-d", binaryRoot], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (not os.path.exists(binaryPath)):
        raise Exception("Failed to extract prebuilt content shell binary")
    return binaryPath

def contentShellBinary(contentShell):
    if (contentShell and os.path.exists(contentShell)):
        return contentShell
    system = platform.system()
    if (system == "Darwin"):
        return unpackPrebuiltContentShellBinary("mac", "72cff265974701c8e6453e8b47a91d03053ea140", "Content Shell.app/Contents/MacOS/Content Shell")
    elif (system == "Linux"):
        if (platform.architecture()[0] == "64bit"):
            return unpackPrebuiltContentShellBinary("linux64", "72cff265974701c8e6453e8b47a91d03053ea140", "content_shell")
    #elif (system == "Windows"):
    #    TODO: Build this.
    raise Exception("Content shell not found. If you have a chromium checkout, you may specify your own content shell binary using --content-shell")

def runContentShell(contentShell, inputPath, additionalFlags):
    command = [contentShell, "--run-layout-test",
               "--enable-font-antialiasing", additionalFlags, inputPath]
    try:
        p = subprocess.Popen(command,
                             shell = False,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        return p.stdout.read()
    except:
        commandString = " ".join(str(c) for c in command) 
        raise Exception("Failed to run content shell (" + commandString + ")")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="chromium-content-screenshot: command line tool for converting html/svg to png")
    parser.add_argument("input", help="input (html file/url, or svg file/url")
    parser.add_argument("output", help="output png file")
    parser.add_argument("--content-shell", dest="contentShell", help="path to content shell binary")
    parser.add_argument("--flags", help="additional flags to pass to content shell")
    parser.add_argument("--width", help="width of rendering (px)", type=int)
    parser.add_argument("--height", help="height of rendering (px)", type=int)
    parser.add_argument("--no-svg-mode", dest="noSvgMode", help="disable special handling of SVG files")
    args = parser.parse_args()

    flags = args.flags if args.flags else ""
    svgMode = args.input.endswith("svg") and not args.noSvgMode
    binary = contentShellBinary(args.contentShell)

    if (svgMode):
        image = svgAsPng(binary, args.input, flags, args.width, args.height)
    else:
        image = htmlAsPng(binary, args.input, flags, args.width, args.height)

    with open(args.output, "wb") as outputFile:
        outputFile.write(image)
        print "Done"