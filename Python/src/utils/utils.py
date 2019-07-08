""""
This file implements all the auxiliar functions
"""

import os
import sys


# pylint: disable=no-member
# pylint: disable=protected-access
# pylint: disable=broad-except
def get_absolute_resource_path(relative_path):
    """
    Function to handle the pyinstaller added data relative path
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        try:
            base_path = os.path.dirname(sys.modules['src'].__file__)
        except Exception:
            base_path = ''

        if not os.path.exists(os.path.join(base_path, relative_path)):
            base_path = 'src'

    path = os.path.join(base_path, relative_path)

    if not os.path.exists(path):
        return None

    return path
