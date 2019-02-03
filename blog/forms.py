from django import forms
from .models import Post 
from .models import Comment 
from django.contrib.auth import models as auth_models
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','text')


class LoginForm(forms.Form):   #추가
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

class CreateUserForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    email = forms.EmailField(required=True) # 이메일 필드 추가

    class Meta:
        model = auth_models.User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super().save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user