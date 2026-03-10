import contextlib
import io

from roboticstoolbox.tools import *
from roboticstoolbox.tools import __all__ as tools_all

__all__ = [*tools_all]

try:
    with contextlib.redirect_stderr(io.StringIO()):
        from roboticstoolbox.robot import *
        from roboticstoolbox.robot import __all__ as robot_all
except ImportError:
    robot_all = []
else:
    __all__.extend(robot_all)

try:
    with contextlib.redirect_stderr(io.StringIO()):
        from roboticstoolbox.mobile import *
        from roboticstoolbox.mobile import __all__ as mobile_all
except ImportError:
    mobile_all = []
else:
    __all__.extend(mobile_all)

try:
    with contextlib.redirect_stderr(io.StringIO()):
        from roboticstoolbox import models
except ImportError:
    pass
else:
    __all__.append("models")

try:
    with contextlib.redirect_stderr(io.StringIO()):
        from roboticstoolbox import backends
except ImportError:
    pass
else:
    __all__.append("backends")

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("roboticstoolbox-python")
except importlib.metadata.PackageNotFoundError:
    pass
