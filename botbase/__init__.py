### TODO: test Q/S/I support
### TODO: rewrite update() to use a batch request
import datetime, dateutil.parser, sys
today = datetime.date.today # today() function shorthand
from datetime import datetime

# Google sheets oauth authorization
from .oauth import googlesheets

# Scheduler may need to update this
#todaystr = time.strftime("%d.%m.%Y")

# Used by scheduler, allow filling in modules
schedule = []
from .task import Task, Hourly

from .sheets import *
from .parse import *
from .crawlutil import *
