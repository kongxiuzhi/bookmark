from django.conf.urls import url
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
		#url(r'^login/$',views.userLogin,name="login"),
		url(r'^users/$',views.user_list,name="user_list"),
		url(r'^users/follow/$',views.user_follow,name='user_follow'),
		url(r'^users/(?P<username>[-\w]+)/$',views.user_detail,name='user_detail'),
		url(r'^register/$',views.register,name="register"),
		url(r'^edit/$',views.edit,name="edit"),
		url(r'^login/$',authViews.login,name="login"),
		url(r'^logout$',authViews.logout,name="logout"),
		url(r'^logoutAndLogin/$',authViews.logout_then_login,name="logout_then_login"),
		url(r'^$',views.dashboard,name="dashboard"),
		url(r'^passwordChange/$',authViews.password_change,name="password_change"),
		url(r'^passwordChange/done/$',authViews.password_change_done,name="password_change_done"),
		url(r'^passwordReset/$',authViews.password_reset,name="password_reset"),
		url(r'^passwordReset/done/$',authViews.password_reset_done,name="password_reset_done"),
		url(r'^passwordReset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',authViews.password_reset_confirm,name="password_reset_confirm"),
		url(r'^passwordReset/complete/$',authViews.password_reset_complete,name="password_reset_complete"),
	]