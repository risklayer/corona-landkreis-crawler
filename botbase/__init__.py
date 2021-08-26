### TODO: test Q/S/I support
### TODO: rewrite update() to use a batch request
import time, sys

# Google sheets oauth authorization
from .oauth import googlesheets

# Scheduler may need to update this
todaystr = time.strftime("%d.%m.%Y")

# Used by scheduler, allow filling in modules
schedule = []
from .task import Task

from .sheets import *
