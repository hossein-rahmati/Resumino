from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "پروفایل"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "get_headline")

    def get_headline(self, instance):
        if hasattr(instance, "profile"):
            return instance.profile.headline
        return "-"
    get_headline.short_description = "عنوان شغلی"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "headline", "phone_number", "created_at")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "headline", "phone_number")
    list_filter = ("created_at",)

