#!/usr/bin/env python

import hashlib
import unittest
import contentScreenshot

class TestSvgOutput(unittest.TestCase):
    def setUp(self):
        # Use a prebuilt content shell by default
        self.contentShellBinary = contentScreenshot.contentShellBinary(None)

    def imageMd5(self, image):
        return hashlib.md5(image).hexdigest()

    def fileMd5(self, inFile):
        return hashlib.md5(open(inFile, "rb").read()).hexdigest()

    def test_svgWidthAndHeight(self):
        image = contentScreenshot.svgAsPng(self.contentShellBinary, "test/greenSquare.svg", "", 200, 200)
        expected = self.fileMd5("test/200x200greenSquare.png")
        self.assertEqual(self.imageMd5(image), expected)

    def test_svgWidthWithoutHeight(self):
        image = contentScreenshot.svgAsPng(self.contentShellBinary, "test/greenSquare.svg", "", 200, None)
        expected = self.fileMd5("test/200x200greenSquare.png")
        self.assertEqual(self.imageMd5(image), expected)

    def test_svgTransparency(self):
        image = contentScreenshot.svgAsPng(self.contentShellBinary, "test/greenCircle.svg", "", None, 50)
        expected = self.fileMd5("test/50x50greenCircle.png")
        self.assertEqual(self.imageMd5(image), expected)

    def test_htmlWidthAndHeight(self):
        image = contentScreenshot.htmlAsPng(self.contentShellBinary, "test/greenSquare.html", "", 100, 100)
        expected = self.fileMd5("test/100x100greenSquare.png")
        self.assertEqual(self.imageMd5(image), expected)

    def test_htmlBackgroundIsWhite(self):
        image = contentScreenshot.htmlAsPng(self.contentShellBinary, "test/greenSquare.html", "", 150, 150)
        expected = self.fileMd5("test/greenSquareOnWhiteBackground.png")
        self.assertEqual(self.imageMd5(image), expected)

    def test_htmlSizeFlag(self):
        image = contentScreenshot.htmlAsPng(self.contentShellBinary, "test/greenSquare.html", "--content-shell-host-window-size=100x100", None, None)
        expected = self.fileMd5("test/100x100greenSquare.png")
        self.assertEqual(self.imageMd5(image), expected)

    def test_missingBinary(self):
        self.assertRaises(Exception, contentScreenshot.htmlAsPng, (None, "test/greenSquare.html", "", None, None))
        self.assertRaises(Exception, contentScreenshot.svgAsPng, (None, "test/greenSquare.svg", "", None, None))

if __name__ == "__main__":
    unittest.main()