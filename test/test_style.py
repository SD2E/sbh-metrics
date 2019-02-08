import unittest

import pycodestyle


class TestStyle(unittest.TestCase):

    def test_style(self):
        """Run pycodestyle on the directory tree."""
        # If there are files that don't have the '.py' extension, add
        # them to dirs_and_files to include them in the style checks.
        dirs_and_files = ['.']
        # Allow 120 character lines. The default is 80, but that's a
        # pretty narrow window size these days.
        sg = pycodestyle.StyleGuide(quiet=True, max_line_length=119)
        report = sg.check_files(dirs_and_files)
        self.assertEqual(report.total_errors, 0)


if __name__ == '__main__':
    unittest.main()
