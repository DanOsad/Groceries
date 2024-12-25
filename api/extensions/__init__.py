#### PREVENT PYCACHE ####
import sys
sys.dont_write_bytecode = True

#### ADD PYTHONPATH ####
sys.path.append('/tools/python/packages/lib/python3.6/site-packages/')

from .setup import app, db, FlaskApp#, Response
from .response import Response, Success, Failure
# from .monitor import PerformanceMonitor
from .constants import HTTPStatusCode

tools = FlaskApp()
# perf_mon  = PerformanceMonitor()