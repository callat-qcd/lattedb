from django.contrib import admin

# Register your models here.
from espressodb.base.admin import register_admins


register_admins("lattedb.fermionaction")
