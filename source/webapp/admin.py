from django.contrib import admin

from webapp.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ("author", "description", "picture")


admin.site.register(Comment)
