from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/%Y/%m/", blank=True, null=True, verbose_name="تصویر پروفایل")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="شماره تماس")
    headline = models.CharField(max_length=150, blank=True, verbose_name="عنوان شغلی")
    bio = models.TextField(blank=True, verbose_name="درباره من")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "پروفایل کاربری"
        verbose_name_plural = "پروفایل‌های کاربری"

    def __str__(self):
        return f"پروفایل {self.user.username}"

    def get_display_name(self):
        full_name = self.user.get_full_name().strip()
        if full_name:
            return full_name
        return self.user.username

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        display_name = self.get_display_name()
        return f"https://ui-avatars.com/api/?name={display_name}&background=2563eb&color=fff&size=128"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)

