from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from sleighmeapi.views import register_user, login_user
from sleighmeapi.views.gift_preference import GiftPreferenceView
from sleighmeapi.views.group import GroupView
from sleighmeapi.views.member import MemberView
from sleighmeapi.views.profiles import ProfileView
from sleighmeapi.views.states import StateView
from sleighmeapi.views.user import UserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'groups', GroupView, 'group')
router.register(r'users', UserView, 'user')
router.register(r'members', MemberView, 'member')
router.register(r'profiles', ProfileView, 'profiles')
router.register(r'gift_preferences', GiftPreferenceView, 'gift_preference')
router.register(r'states', StateView, 'state')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]
