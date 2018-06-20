# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.conf import settings
from django.shortcuts import render


def welcome(request):
    root_dir = getattr(settings, 'BASE_DIR', '')
    template_name = os.path.join(root_dir, 'patch/templates/index.html')
    return render(request, template_name)