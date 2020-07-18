from django.contrib import admin
from .models import Post, AdditionalImage
from .models import Comment

class AdditionalImageInline(admin.TabularInline):
	model = AdditionalImage

class PostAdmin(admin.ModelAdmin):
	list_display = (
		'title',
		'content',
		'author',
		'created_at')

	inlines = (AdditionalImageInline,)

	fields = (
		('title', 'author'),
		'content',
		 'image')
	
	readonly_fileds = ('created_at',)

class CommentAdmin(admin.ModelAdmin):
	list_display = (
		'post',
		'author',
		'content',
		'created_at')
	fields = (
		('post', 'author'),
		'content',
		'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

# Register your models here.
