from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.auth import views as auth_views
from .views import  PasswordChangeView,UserEditView,PasswordResetView
from django.conf import settings
from django.conf.urls.static import static
# from django.views.decorators.csrf import csrf_exempt
admin.site.site_header="Forum Admin"
admin.site.site_title="Forum Admin Panel"
admin.site.index_title="Welcome to Forum Admin Panel"
urlpatterns = [
    path('', views.home, name="home"),
    # path('home',views.home2, name="home2"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('search', views.search, name="search"),
    # path('search', views.search, name="search"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('password/',PasswordChangeView.as_view(template_name="registration/passwordchange.html")),
    path('view_profile', views.view_profile, name="view_profile"),
    path('edit_profile',UserEditView.as_view(), name="edit_profile"),
    path('password_success',views.password_success,name="password_success"),
    path('edit_success',views.edit_success,name="edit_success"),
    path('ask-question', views.askquestion),
    path("category/<slug:category>", views.category),
    path('question/<int:qid>/<slug:qslug>', views.viewquestion),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/passwordconfirm.html'), name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),
     name='password_reset_complete'),
    #path('detect', views.detect, name = 'detect disease'),
    #path('detected', views.detected, name = 'disease detected')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)