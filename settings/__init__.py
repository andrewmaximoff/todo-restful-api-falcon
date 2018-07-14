# -* coding: utf-8 *-
"""
Config import handler
This let us import settings, and don't care about:
>>> settings = importlib.import_module('module_name')
"""
import os
import importlib


# Settings
DEBUG = False

MONGO = {
    'DATABASE': os.getenv('TODOAPI_MONGO_DATABASE') or 'test',
    'HOST': os.getenv('TODOAPI_MONGO_HOST') or '127.0.0.1',
    'PORT': os.getenv('TODOAPI_MONGO_PORT') or 27017,
    'USERNAME': os.getenv('TODOAPI_MONGO_USERNAME') or 'admin',
    'PASSWORD': os.getenv('TODOAPI_MONGO_PASSWORD') or ''
}

my_module = importlib.import_module(os.getenv('SETTINGS_MODULE'))

my_module_dict = my_module.__dict__

try:
    to_import = my_module.__all__
except AttributeError:
    to_import = [name for name in my_module_dict if not name.startswith('_')]

globals().update({name: my_module_dict[name] for name in to_import})
