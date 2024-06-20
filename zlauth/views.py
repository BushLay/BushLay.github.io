import random
import string

from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from zlauth.forms import RegisterForm, LoginForm
from zlauth.models import CaptchaModel

User = get_user_model()

# Create your views here.


def zllogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)

                # 判断是否需要记住我
                if not remember:
                    # 如果未点击记住我，设置过期时间为0
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('邮箱或密码错误!')
                form.add_error('email', '邮箱或密码错误!')
                return render(request, 'login.html', context={'form': form})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('zlauth:register'))

def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    # 生成验证码
    captcha = "".join(random.sample(string.digits, 4))
    # 存储到数据库中
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("知了博客注册验证码", message=f"您的注册验证码是: {captcha}", from_email=None, recipient_list=[email])


    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})










