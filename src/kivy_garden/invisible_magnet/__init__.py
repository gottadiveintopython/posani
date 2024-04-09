__all__ = (
    'magnetize', 'unmagnetize', 'is_magnetized',
    'install', 'uninstall', 'uninstall_all',
)

from ._main import magnetize, unmagnetize, is_magnetized
from ._install import install, uninstall, uninstall_all
