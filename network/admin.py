from django.contrib import admin
from .models import Post, Like, Follow, User


class FollowAdmin(admin.ModelAdmin):
  filter_horizontal=("follower",)
    
# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow, FollowAdmin)
admin.site.register(User)