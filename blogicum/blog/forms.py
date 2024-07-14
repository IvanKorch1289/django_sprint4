from django.forms import DateInput, ModelForm

from blog.models import Post, Comment, User


class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {'pub_date': DateInput(attrs={'type': 'date'})}


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
