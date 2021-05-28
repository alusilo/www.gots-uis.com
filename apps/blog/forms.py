from django import forms

from apps.blog.models import Comment

# Register your models here.
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')

