from django.urls import path, include
from rest_framework import routers
from .views import (
	CurrentUserView, PostViewSet, UserStatsView, RandomPublicPostView
)


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
	path('auth/', include('rest_auth.urls')),
	path('user/', CurrentUserView.as_view()),
	path('stats/', UserStatsView.as_view()),
	path('posts/random_public/', RandomPublicPostView.as_view()),
	path('', include(router.urls)),
]
