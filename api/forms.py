from django import forms
from .models import Post

#Form to create posts
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        #define fields
        fields = ['title','content',]

    #function to prevent posts with hack in the content or title
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if 'hack' in title.lower():

            return None
        return title
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if 'hack' in content.lower():

            return None
        return content