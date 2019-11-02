from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['about_user', 'link_to_github', 'avatar']


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
