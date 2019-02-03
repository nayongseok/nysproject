from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/',views.post_read, name='post_read'),                           
    path('post_form', views.post_form, name='post_form'),       
    path('post/<int:post_id>/edit',views.post_edit, name='post_edit'),                           
    path('post_delete/<int:post_id>/delete',views.post_delete, name='post_delete'),
    path('about/', views.about, name="about"),
    path('like/', views.like, name="like"),
    path('hate/', views.hate, name="hate"),
    path('post/<int:post_id>/comment', views.add_comment_to_post, name='add_comment_to_post'), 
    path('comment/<int:comment_id>/delete/', views.comment_delete, name="comment_delete"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('blog/permission_denied/',views.permission_denied, name="permission_denied"),

    # test
    path('signup/', views.CreateUserView.as_view(), name='signup')
    
]
 