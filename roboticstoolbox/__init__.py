from roboticstoolbox.tools import *
from roboticstoolbox.tools import __all__ as tools_all
from roboticstoolbox.robot import *
from roboticstoolbox.robot import __all__ as robot_all
from roboticstoolbox.mobile import *
from roboticstoolbox.mobile import __all__ as mobile_all
from roboticstoolbox import models
from roboticstoolbox import backends

__all__ = list(tools_all)
__all__.extend(robot_all)
__all__.extend(mobile_all)
__all__.append("models")
__all__.append("backends")

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("roboticstoolbox-python")
except importlib.metadata.PackageNotFoundError:
    pass
