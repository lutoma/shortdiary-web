from django.urls import path, include
from rest_framework import routers
from .views import (
	CurrentUserView, PostViewSet, RandomPublicPostView
)


app_name = 'apiv2'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
	path('auth/', include('rest_auth.urls')),
	path('user/', CurrentUserView.as_view()),
# 	path('stats/', UserStatsView.as_view()),
	path('posts/random_public/', RandomPublicPostView.as_view(), name='posts-random'),
	path('', include(router.urls)),
]
