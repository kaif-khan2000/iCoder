from django.urls import path
from . import views
urlpatterns = [
    path('',views.blogHome,name='blogHome'),

    #api to post comment
    path('postComment',views.postComment,name='postComment'),
    
    path('<str:slug>',views.blogPost,name='blogPost'),

]
