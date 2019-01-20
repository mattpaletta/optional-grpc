import os
IS_RUNNING_LOCAL = not os.path.exists("/.dockerenv")
from optionalgrpc.service import Service

__all__ = [Service]
