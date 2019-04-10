#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""backend URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.urls import path

from .bad.views import BadView
from .good.views import GoodView
from .insufficient.views import InsufView
from .utils import require_query_uniqueness

urlpatterns = [
    path('bad', require_query_uniqueness(BadView.as_view()), name="bad"),
    path('good', require_query_uniqueness(GoodView.as_view()), name="good"),
    path('insuf', require_query_uniqueness(InsufView.as_view()), name="insuf"),
]
