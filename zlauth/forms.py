from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '请传入用户名!',
        'min_length': '用户名长度在2~20之间!',
        'max_length': '用户名长度在2~20之间!'
    })
    email = forms.EmailField(error_messages={"required": '请传入邮箱!', 'invalid': '请传入一个正确的邮箱!'})
    captcha = forms.CharField(min_length=4, max_length=4)
    password = forms.CharField(min_length=6, max_length=20)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经被注册!')
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": '请传入邮箱!', 'invalid': '请传入一个正确的邮箱!'})
    password = forms.CharField(min_length=6, max_length=20)
    remember = forms.IntegerField(required=False)