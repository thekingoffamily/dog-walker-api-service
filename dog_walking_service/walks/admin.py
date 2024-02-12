from django.contrib import admin
from .models import WalkOrder, APICall, Walker

admin.site.register(WalkOrder)
admin.site.register(APICall)
admin.site.register(Walker)