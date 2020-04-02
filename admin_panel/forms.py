from django.contrib.gis import forms as geoforms


class RequestForm(geoforms.Form):
    radius = geoforms.IntegerField()
    location = geoforms.PointField(widget=geoforms.OSMWidget({'map_srid': 4326}), required=True)
