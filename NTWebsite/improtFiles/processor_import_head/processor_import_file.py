from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.cache import caches
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import QueryDict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import Template, Context, RequestContext

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection

from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.MainMethods import RedisCacheOperation as QCO
from NTWebsite.improtFiles.models_import_head import *
#from NTWebsite import Config as aConf
from NTWebsite import MainMethods as mMs
from NTWebsite.models import *
from NTNotification.Processor import *

from PIL import Image as im
from NTConfig import settings
from collections import Iterable

import sys
import os
import base64
import uuid
import time
import json
import redis
