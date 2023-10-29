from django.contrib import admin

from .models import *

admin.site.register(Vote)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(VoteResult)
