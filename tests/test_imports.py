#!/usr/bin/env python3
"""
@author: Jesse Haviland
"""

import subprocess
import sys
import textwrap
import unittest


class TestImports(unittest.TestCase):
    def test_numpy2_import_order(self) -> None:
        script = textwrap.dedent(
            """
            import spatialmath.base as smb
            import numpy as np
            import roboticstoolbox as rtb

            print(smb.__name__, np.__version__, rtb.__name__)
            """
        )

        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            check=False,
            text=True,
        )
        parts = result.stdout.strip().split()

        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertEqual(parts[0], "spatialmath.base")
        self.assertRegex(parts[1], r"^\d+\.\d+(\.\d+)?$")
        self.assertEqual(parts[2], "roboticstoolbox")


if __name__ == "__main__":  # pragma nocover
    unittest.main()
