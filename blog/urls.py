# from django.urls import path
#
# import blog.views
#
# app_name = 'blog'
#
# urlpatterns = [
#     path("index/", blog.views.index, name="index"),
#     path("", blog.views.index, name="index"),
#     path("blog/detail/<int:blog_id>/", blog.views.blog_detail, name="blog_detail"),
#     path("blog/pub/", blog.views.pub_blog, name="pub_blog"),
#     path("blog/comment/pub/", blog.views.blog_comment, name="blog_comment"),
# ]


from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("index/", views.index, name="index"),
    path("", views.index, name="index"),
    path("blog/detail/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("blog/pub/", views.pub_blog, name="pub_blog"),  # 确保URL以斜杠结尾
    path("blog/comment/pub/", views.blog_comment, name="blog_comment"),
    path("search/", views.search, name="search"),
]
