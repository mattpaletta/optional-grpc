import os
IS_RUNNING_LOCAL = not os.path.exists("/.dockerenv")
ONE_DAY_IN_SECONDS = 60 * 60 * 24