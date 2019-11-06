# pylint: disable=C0103
"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from lattedb.project.formfac.views import IndexView, DiskStatusView, TapeStatusView

app_name = "Project formfac"
urlpatterns = [
    path("", IndexView.as_view(), name="Form Factor"),
    path("disk-status", DiskStatusView.as_view(), name="Form Factor Disk Status"),
    path("tape-status", TapeStatusView.as_view(), name="Form Factor Tape Status"),
]
