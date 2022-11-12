from django.contrib import admin
from base.models import Nutrition, Upload, User, Extract

# Register your models here.
admin.site.register(User)
admin.site.register(Extract)
admin.site.register(Upload)
admin.site.register(Nutrition)
