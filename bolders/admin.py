from django.contrib import admin
from bolders.models import Post, Character

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'ingamedate', 'timestamp')
    search_fields = ['title', 'content']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
admin.site.register(Character)
# Register your models here.
