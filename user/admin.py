from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

# Optional: Inline to show/edit role on the User admin page
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the default UserAdmin to include UserProfile inline
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class UserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline,)

# Unregister the default User admin, then register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Also register UserProfile separately (optional)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    search_fields = ['user__username', 'role']