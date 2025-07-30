from django import forms
from .models import Post
from .models import Comment
from .models import Image
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your comment...'}),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['title','description','image_file','tags']