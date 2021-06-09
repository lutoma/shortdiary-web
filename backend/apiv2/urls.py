from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
	CurrentUserView, PostViewSet, PostImageViewSet, RandomPublicPostView,
	LeaderboardView, SignupView
)

app_name = 'apiv2'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'post_images', PostImageViewSet, basename='post_images')

urlpatterns = [
	path('auth/', include('trench.urls')),
	path('auth/', include('trench.urls.simplejwt')),
	path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

	path('user/', CurrentUserView.as_view()),
	path('user/signup/', SignupView.as_view()),
	path('posts/random_public/', RandomPublicPostView.as_view(), name='posts-random'),
	path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
	path('', include(router.urls)),
]
