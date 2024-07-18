from django.forms import DateTimeInput, ModelForm, Textarea
from django.utils import timezone

from blog.models import Comment, Post, User


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.now()

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {'pub_date': DateTimeInput(
            format='%Y-%m-%d',
            attrs={'class': 'form-control',
                   'type': 'datetime-local'
                   }
        )}


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': Textarea(attrs={'cols': 10, 'rows': 5})}


class ProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
