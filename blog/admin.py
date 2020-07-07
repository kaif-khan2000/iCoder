from django.contrib import admin
from .models import Post,BlogComment
# Register your models here.
admin.site.register(BlogComment)
@admin.register(Post)
class POstAdmin(admin.ModelAdmin):
    class Media:
        js = ("tinymce.js",)