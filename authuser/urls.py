from django.urls import path
from authuser import views
from .views import user_login


urlpatterns = [
    path("signup/", views.signup , name='signup'),
    path("login/", user_login.as_view() , name='user_login'),
    path("logout/", views.handlelogout , name='user_logout'),
    path('activate/<uidb64>/<token>', views.ActivateAccountViews.as_view(), name ='activate'),
    path('not/', views.page_not_found , name='pagenotfound' ),
    path('changepass/', views.changepass , name='change_password' ),
    path('profile', views.Profile.as_view() , name="profile"),
    path('callme', views.call_me, name="callme"),
]