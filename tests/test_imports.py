#!/usr/bin/env python3
"""
@author: Jesse Haviland
"""

import builtins
from pathlib import Path
import subprocess
import sys
import textwrap
import tomllib
from typing import Any
import types
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
PACKAGE_INIT = REPO_ROOT / "roboticstoolbox" / "__init__.py"


class TestImports(unittest.TestCase):
    def test_dependency_metadata_uses_numpy2_and_spatialgeometry_fork(self) -> None:
        pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
        project_deps = pyproject["project"]["dependencies"]
        build_requires = pyproject["build-system"]["requires"]

        self.assertIn("numpy>=2.0.0", project_deps)
        self.assertIn(
            "spatialgeometry @ git+https://github.com/gaurishg/spatialgeometry.git@main",
            project_deps,
        )
        self.assertIn("numpy>=2.0.0", build_requires)

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

    def test_top_level_import_propagates_robot_import_errors(self) -> None:
        package_source = PACKAGE_INIT.read_text(encoding="utf-8")
        fake_tools = types.ModuleType("roboticstoolbox.tools")
        fake_tools.__all__ = []
        original_import = builtins.__import__

        def fake_import(
            name: str,
            globals: dict[str, Any] | None = None,
            locals: dict[str, Any] | None = None,
            fromlist: tuple[str, ...] = (),
            level: int = 0,
        ) -> Any:
            if name == "roboticstoolbox.tools":
                return fake_tools
            if name == "roboticstoolbox.robot":
                raise ImportError("NumPy ABI mismatch")
            return original_import(name, globals, locals, fromlist, level)

        builtins_dict = dict(vars(builtins))
        builtins_dict["__import__"] = fake_import

        with self.assertRaisesRegex(ImportError, "NumPy ABI mismatch"):
            exec(
                compile(package_source, str(PACKAGE_INIT), "exec"),
                {
                    "__name__": "roboticstoolbox",
                    "__package__": "roboticstoolbox",
                    "__builtins__": builtins_dict,
                },
            )


if __name__ == "__main__":  # pragma nocover
    unittest.main()
