from django.urls import path
from . import views

urlpatterns = [
    path('',views.index , name='indexBlog'),
    path('blog/contact/' , views.contact , name='contactUs'),
    path('blog/about/' , views.about , name='aboutUs'),
    path('blog/blogs/' , views.blogs , name='blogs'),
    path('blog/register/',views.register , name='register'),
    path('blog/login/',views.login_user , name='login'),
    path('blog/blogs/addblog/',views.addblog , name='addblog'),
    path('blog/logout_user/',views.logout_user , name='logout'),
    path('blog/search/',views.search , name='search'),
    path('blog/postComment/',views.postComment , name='postComment'),
    path('blog/myblog/',views.myblog , name='myblog'),
    path('blog/blogs/<slug:slug>/',views.blogpost , name='blogpost'),
]