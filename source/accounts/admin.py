from django.contrib import admin

from accounts.models import Gender
from accounts.models import Profile

admin.site.register(Gender)
admin.site.register(Profile)
