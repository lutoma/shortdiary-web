from django.urls import path, include
from rest_framework import routers
from .views import (
	CurrentUserView, PostViewSet, RandomPublicPostView, LeaderboardView
)

app_name = 'apiv2'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
	path('auth/', include('trench.urls')),
	path('auth/', include('trench.urls.simplejwt')),

	path('user/', CurrentUserView.as_view()),
	path('posts/random_public/', RandomPublicPostView.as_view(), name='posts-random'),
	path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
	path('', include(router.urls)),
]
