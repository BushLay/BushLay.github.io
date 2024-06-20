from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from blog.forms import PubBlogForm
from blog.models import BlogCategory, Blog, BlogComment


# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={'blogs': blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', {'blog': blog})

@login_required()
def pub_blog(request):
    return render(request, 'pub_blog.html')


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_id = form.cleaned_data['category']
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "博客发布成功！", "data":{"blog_id": blog.id}})



@require_POST
@login_required()
def blog_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)
    return redirect(reverse('blog:blog_detail', kwargs={"blog_id":blog_id}))


@require_GET
def search(request):
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, "index.html", context={"blogs": blogs})