from django.contrib import admin
from . import models
from django.contrib.gis.db.models import PointField
from mapwidgets.widgets import GooglePointFieldWidget


class RequestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        # PointField: {"widget": GooglePointFieldWidget}
    }


admin.site.register(models.Request, RequestAdmin)
admin.site.register(models.Category)
admin.site.register(models.Comment)
