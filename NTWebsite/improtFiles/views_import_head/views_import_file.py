from django.shortcuts import render_to_response, render
from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.Config import AppConfig as AC
from NTWebsite.Config import DBConfig as DC

from NTWebsite.improtFiles.models_import_head import *
#from NTWebsite import AppConfig as aConf
from NTWebsite import MainMethods as mMs
from NTWebsite import Processor as P
from NTWebsite import AccessSizer as A
from NTWebsite.models import *

