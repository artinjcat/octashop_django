from django.urls import path

from auth.users.views.site import (
  login_user, logout_user, register_user, profile_user, update_password, edit_profile_user, favorites, rules_page, verify_phone_number
  )


urlpatterns = [
    path('login/',login_user, name='login'),
    path('logout/',logout_user, name='logout'),
    path('register/',register_user, name='register'),
    path('verify-phone-number/',verify_phone_number, name='verify-phone-number'),
    path('profile/',profile_user, name='profile'),
    path('update-password/',update_password, name='update-password'),
    path('edit-profile/',edit_profile_user, name='edit-profile'),
    path('favorites/',favorites, name='favorites'),

    path('rules/',rules_page, name='rules'),
  

]