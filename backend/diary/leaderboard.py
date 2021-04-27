from diary.models import DiaryUser, Post
from django.db.models import Avg, Count
from django.db.models.functions import Cast, Length
from django.db.models import IntegerField
from django.core.cache import cache
from operator import itemgetter
from django.db.models import Q
import datetime


def update_leaderboard():
	users = DiaryUser.objects.filter(include_in_leaderboard=True)

	number_of_posts = users \
		.annotate(num_posts=Count('posts')) \
		.filter(num_posts__gt=0) \
		.order_by('-num_posts') \
		.values('username', 'num_posts')[:10]

	average_post_length = users \
		.annotate(avg_length=Cast(Avg(Length('posts__text')), IntegerField())) \
		.filter(avg_length__gt=0) \
		.order_by('-avg_length') \
		.values('username', 'avg_length')[:10]

	# FIXME Turn this into a QuerySet… somehow. Maybe store streak in database
	streak_leaders = [{'username': x.username, 'streak': x.get_streak()} for x in users]
	streak_leaders = filter(itemgetter('streak'), streak_leaders)
	streak_leaders = sorted(streak_leaders, key=itemgetter('streak'), reverse=True)[:10]

	popular_languages = Post.objects \
		.filter(~Q(natural_language=''), natural_language__isnull=False) \
		.values('natural_language') \
		.annotate(count=Count('natural_language')) \
		.order_by('-count')

	popular_locations = Post.objects \
		.filter(~Q(location_verbose='')) \
		.values('location_verbose') \
		.annotate(count=Count('location_verbose')) \
		.order_by('-count')

	cache.set('leaderboard', {
		'number_of_posts': number_of_posts,
		'average_post_length': average_post_length,
		'longest_current_streak': streak_leaders,
		'popular_languages': list(popular_languages),
		'popular_locations': list(popular_locations),
		'last_update': datetime.datetime.now(),
	})
