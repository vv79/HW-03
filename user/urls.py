from django.urls import path
from .views import (UserLoginView,
                    UserLogoutView,
                    UserRegistrationView,
                    UserProfileView,
                    UserPasswordChangeView,
                    UserUpgradeView,
                    UserDowngradeView)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/change-password/', UserPasswordChangeView.as_view(), name='change_password'),
    path('profile/up/', UserUpgradeView.as_view(), name='upgrade_user'),
    path('profile/down/', UserDowngradeView.as_view(), name='downgrade_user'),
]
