from django.contrib import admin
from comments.models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'text', 'post']


admin.site.register(Comment, CommentAdmin)
