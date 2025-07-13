#!/usr/bin/env python3
"""Celery configuration for Django project"""

import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app_0x03.settings')

app = Celery('alx_travel_app_0x03')

# Load settings from Django settings.py with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
