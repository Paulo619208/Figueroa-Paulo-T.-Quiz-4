from django import forms
from .models import Post, Comment # ✅ 1. IMPORT THE COMMENT MODEL

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "What's on your mind?"}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

# ✅ 2. ADD THIS NEW FORM FOR COMMENTS
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment...'}),
        }