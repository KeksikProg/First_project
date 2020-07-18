from django.urls import path
from .views import home
from .views import other
from .views import add
from .views import detail
from .views import post_delete
from .views import post_change
from .views import UserRegister
from .views import PostLogin
from .views import PostLogout
from .views import ChangeUserInfo
from .views import DeleteUserView 
from .views import UserPasswordChange
from .views import comment_delete

urlpatterns = [
	path('', home, name = 'home'),	
	path('other/<str:page>/', other, name = 'other'),
	path('posts/add/', add, name = 'add'),
	path('posts/detail/<int:pk>', detail, name = 'detail'),
	path('posts/delete/<int:pk>', post_delete, name = 'delete'),
	path('posts/change/<int:pk>', post_change, name = 'change'),
	path('profile/add/', UserRegister.as_view(), name = 'register'),
	path('profile/login/', PostLogin.as_view(), name = 'login'),
	path('profile/logout', PostLogout.as_view(), name = 'logout'),
	path('profile/change', ChangeUserInfo.as_view(), name = 'changeuser'),
	path('profile/delete', DeleteUserView.as_view(), name ='deleteuser'),
	path('profile/cpassword', UserPasswordChange.as_view(), name = 'changepassword'),
	path('posts/comm_delete/<int:comments>', comment_delete, name = 'comm_delete'),
]
