import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import django.contrib.auth
from diary.models import Post, DiaryUser
from diary.forms import PostForm, SignUpForm, AccountSettingsForm
from django.conf import settings
from django.core.cache import cache
import diary.tasks as tasks
from django.db.models import Q, Count, Avg
from django_q.tasks import async_task

from django.utils.translation import get_language_from_request


def index(request):
	context = {'title': None}

	if not request.user.is_authenticated:
		return render(request, 'frontpage.html', context=context)

	return render(request, 'db2.html', context=context)


@login_required
def edit_post(request, post_id=None):
	"""
	Edit or add post.

	This view takes one parameter (post_id). It defaults to None, in which case
	a new post will be created.
	"""

	edit_post = None

	# Do we want to edit an existing post? If yes, try to find that post.
	# (And also check if that post was within the last 7 days)
	if post_id:
		edit_post = get_object_or_404(Post, id=post_id, author=request.user)

		if not edit_post.is_editable():
			raise PermissionDenied

	yesterday = datetime.date.today() - datetime.timedelta(days=1)

	if not request.method == 'POST':
		# Check if there are not already posts existing for the last 2 days
		# This is only relevant if we add a new post
		existing_posts = (
			Post.objects.filter(author=request.user, date=yesterday),
			Post.objects.filter(author=request.user, date=datetime.date.today())
		)

		# Pass this information along to the template, which will show an error
		# if posts for both days exist already (Or will hide the day for which
		# a post already exists, if there's only one).
		context = {
			'title': _('Edit post') if edit_post else _('New post'),
			'post_days': (yesterday, datetime.date.today()),
			'existing_posts': existing_posts,
			'form': PostForm(),
			'edit_post': edit_post,
		}

		return render(request, 'edit_post.html', context=context)

	# Request method is POST
	form = PostForm(request.POST, request.FILES)
	if not form.is_valid():
		context = {
			'title': _('New post'),
			'post_days': (yesterday, datetime.date.today()),
			'form': form,
			'edit_post': edit_post,
		}

		return render(request, 'edit_post.html', context=context)

	if not edit_post:
		# This is a new post, save it
		post = form.save(commit=False)

		if Post.objects.filter(author=request.user, date=post.date).count() > 0:
			return HttpResponse('Sorry, you already have an entry for that day')

		post.author = request.user
		post.save()
	else:
		# This is an edit of an existing post
		edit_post.text = form.cleaned_data['text']
		edit_post.mood = form.cleaned_data['mood']
		edit_post.public = form.cleaned_data['public']
		edit_post.location_lat = form.cleaned_data['location_lat']
		edit_post.location_lon = form.cleaned_data['location_lon']
		edit_post.location_verbose = form.cleaned_data['location_verbose']
		edit_post.save()

	return HttpResponseRedirect('/')


def show_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)

	if not post.public and not request.user.is_authenticated:
		return HttpResponseRedirect('/accounts/login/?next={}'.format(request.get_full_path()))

	if not post.public and post.author != request.user:
		context = {
			'title': _('Sorry! :('),
		}

		return render(request, 'not_public.html', context=context)

	context = {
		'post': post,
		'title': _('Post #{} from {}').format(post.id, post.date),
		'language': post.get_language_name(locale=get_language_from_request(request))
	}

	if post.author == request.user:
		context['title'] = _('Your post #{}').format(post.get_user_id(), post.date)

	return render(request, 'show_post.html', context=context)


def switch_language(request, language):
	request.session['django_language'] = language
	return HttpResponseRedirect('/')


def sign_up(request):
	if not request.method == 'POST':
		context = {
			'title': _('Sign up'),
		}

		return render(request, 'sign_up.html', context=context)

	# Request method is POST
	form = SignUpForm(request.POST, request.FILES)
	if not form.is_valid():
		context = {
			'title': _('Sign up'),
			'form': form,
		}
		return render(request, 'sign_up.html', context=context)

	# Fixme
	user = form.save()
	user.set_password(request.POST.get('password', None))
	user.save()

	user.send_verification_mail()

	login_user = django.contrib.auth.authenticate(username=user.username,
		password=request.POST.get('password', None))

	django.contrib.auth.login(request, login_user)
	return HttpResponseRedirect('/')


def mail_verify(request, user_id, hash):
	user = get_object_or_404(DiaryUser, id=user_id)

	if not hash == user.get_verification_hash():
		return HttpResponse('Sorry, invalid hash.')

	user.mail_verified = True
	user.save()
	return HttpResponseRedirect("/")


@login_required
def account_settings(request):
	if not request.method == 'POST':
		context = {
			'title': _('Account settings'),
			'form': AccountSettingsForm(),
		}
		return render(request, 'account_settings.html', context=context)

	# Request method is POST
	form = AccountSettingsForm(request.POST, request.FILES)

	if not form.is_valid():
		context = {
			'title': _('Account settings'),
			'form': form,
		}
		return render(request, 'account_settings.html', context=context)

	# Save form

	if request.user.email != form.cleaned_data['email']:
		request.user.mail_verified = False
		request.user.email = form.cleaned_data['email']
		request.user.send_verification_mail()

	request.user.geolocation_enabled = form.cleaned_data['geolocation_enabled']
	request.user.save()

	context = {
		'title': _('Account settings'),
		'success': True,
	}
	return render(request, 'account_settings.html', context=context)


@api_view(['DELETE'])
def delete_post(request, post_id):
	"""
	Delete a post. This is currently an AJAX only view
	"""

	# FIXME This should be migrated to the api app.

	post = get_object_or_404(Post, id=post_id, author=request.user)

	if not post.is_editable():
		raise PermissionDenied

	post.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def stats(request):
	user_posts = Post.objects.filter(author=request.user).order_by('date')

	if user_posts.count() < 1:
		return render(request, 'stats_noposts.html')

	top_locations = Post.objects.filter(~Q(location_verbose=''),
		author=request.user).values('location_verbose').annotate(
		location_count=Count('location_verbose')).order_by('-location_count')[:10]

	top_mood_locations = request.user.posts.filter(
		~Q(location_verbose='')).annotate(mood_avg=Avg('mood')).values(
		'location_verbose', 'mood_avg').annotate(location_count=Count(
			'location_verbose')).filter(location_count__gte=3).order_by(
			'-mood_avg').values('location_verbose', 'mood_avg')[:10]

	context = {
		'title': 'Stats',
		'posts': user_posts,
		'top_locations': top_locations,
		'top_mentions': request.user.get_mention_toplist()[:10],
		'top_mood_locations': top_mood_locations,
	}
	return render(request, 'stats.html', context=context)


@login_required
def leaderboard(request):
	leaders = cache.get_many([
		'leaderboard_streak_leaders',
		'leaderboard_posts_leaders',
		'leaderboard_char_leaders',
		'leaderboard_avg_post_length_leaders',
		'leaderboard_last_update',
		'leaderboard_popular_languages',
		'leaderboard_popular_locations',
	])

	if(len(leaders) < 5):
		# Cache is empty, render error page and start async generation of data
		if settings.DEBUG:
			tasks.update_leaderboard()
		else:
			async_task('diary.tasks.update_leaderboard')

		return render(request, 'leaderboard_wait.html')

	context = {
		'title': 'Leaderboard',
		'streak_leaders': leaders['leaderboard_streak_leaders'],
		'posts_leaders': leaders['leaderboard_posts_leaders'],
		'chars_leaders': leaders['leaderboard_char_leaders'],
		'avg_post_length_leaders': leaders['leaderboard_avg_post_length_leaders'],
		'popular_languages': leaders['leaderboard_popular_languages'],
		'popular_locations': leaders['leaderboard_popular_locations'],
		'last_update': leaders['leaderboard_last_update'],
	}

	return render(request, 'leaderboard.html', context=context)


def explore(request):
	post_filters = {'public': True}

	if 'lang' in request.GET:
		post_filters['natural_language'] = request.GET.get('lang', '')

	try:
		post = Post.objects.filter(**post_filters).order_by('?')[:1].get()
	except Post.DoesNotExist:
		return render(request, 'explore_nosuchpost.html')

	context = {
		'title': 'Explore',
		'post': post,
		'language': post.get_language_name(locale=get_language_from_request(request)),
	}
	return render(request, 'show_post.html', context=context)


@login_required
def search(request):
	query = request.GET.get('q', '')
	posts = request.user.posts.filter(text__icontains=query)
	posts.order_by('-date')

	context = {
		'title': 'Search',
		'posts': posts,
	}
	return render(request, 'search_results.html', context=context)
