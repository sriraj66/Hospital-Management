from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index, name="index"),
    path("profile-p/<int:id>", profile, name="profile"),
    path('login/', login_view, name='login'),
    path("accounts/logout/", logout_view, name='logout'),
    path('register/', register, name='register'),
    path('register/doc', register_doc, name='register_doc'),
    path("create-blog",create_blog,name='create_blog'),
    path("view-blog/<int:id>",blog_view,name='view_blog'),
    path("edit-blog/<int:blog_id>",edit_blog,name='edit_blog'),
    path('blog/<int:blog_id>/delete/', delete_blog, name='delete_blog'),
    path("blog-like/<int:id>",like_blog,name='like_blog'),
    path("blog/",all_blogs,name='all_blogs'),
    path("myblog",my_blogs,name='my_blogs'),
    
]
