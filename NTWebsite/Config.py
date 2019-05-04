import os
from .improtFiles.models_import_head import *
#from .MainMethods import QueryDataBaseCache as QDBC
from django.shortcuts import get_object_or_404


class AppConfig(object):
    """docstring for DBConfig"""
    _instance = None

    def __new__(cls, *args, **kwargs):  # 这里不能使用__init__，因为__init__是在instance已经生成以后才去调用的
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        SelectedConfigName = PreferredConfigName.objects.all()[
            0].Name.Name
        ConfigObject = ConfigParams.objects.get(Name=SelectedConfigName)
        FieldNames = []
        for f in ConfigObject._meta.get_fields():
            if f.related_model is None:
                exec("self.%s = ConfigObject.%s" % (f.name, f.name))
                FieldNames.append(f.name)
        self.ConfigNames = FieldNames


class DBConfig(object):
    """docstring for AppConfig"""
    _instance = None

    def __new__(cls, *args, **kwargs):  # 这里不能使用__init__，因为__init__是在instance已经生成以后才去调用的
        if cls._instance is None:
            cls._instance = super(DBConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self, keyword):
        QueryObject = get_object_or_404(FilterQueryString, Name=keyword)
        self.MethodString = QueryObject.MethodString
        self.QueryString = QueryObject.QueryString
        self.Template = QueryObject.Template


