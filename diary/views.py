# coding: utf-8
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from inviteman.models import Invite
import django.contrib.auth
from diary.models import Post
from diary.forms import PostForm, SignUpForm, LoginForm, AccountSettingsForm

tos = lambda request: render_to_response(
		'tos.html',
		context_instance = RequestContext(request, {'title': _('Terms of service')}),
	)

about = lambda request: render_to_response(
		'about.html',
		context_instance = RequestContext(request, {'title': _('About shortdiary')}),
	)

def index(request):
	try:
		randompost = Post.objects.filter(author__userprofile__public = True).order_by('?')[:1].get()
	except Post.DoesNotExist:
		randompost = None

	if not request.user.is_authenticated():
		context = {
			'title': _('It\'s your life. You should remember it.'),
			'post': randompost,
		}
		return render_to_response('frontpage.html', context_instance=RequestContext(request, context))

	context = {
		'title': 'Home',
		'randompost': randompost,
		'posts': Post.objects.filter(author = request.user, date__gte = datetime.date.today() - datetime.timedelta(days = 6)).order_by('-date', '-created_at'),
	}
	return render_to_response('index.html', context_instance=RequestContext(request, context))

@login_required
def edit_post(request, post_id = None):
	"""
	Edit or add post.

	This view takes one parameter (post_id). It defaults to None, in which case
	a new post will be created.
	"""

	edit_post = None

	# Do we want to edit an existing post? If yes, try to find that post.
	# (And also check if that post was within the last 7 days)
	if post_id:
		edit_post = get_object_or_404(Post,
			id = post_id,
			author = request.user,
		)

		if not edit_post.is_editable():
			raise PermissionDenied

	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	
	if not request.method == 'POST':
		# Check if there are not already posts existing for the last 2 days
		# This is only relevant if we add a new post
		existing_posts = (
			Post.objects.filter(author = request.user, date = yesterday),
			Post.objects.filter(author = request.user, date = datetime.date.today())
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

		return render_to_response('edit_post.html', context_instance=RequestContext(request, context))

	# Request method is POST
	form = PostForm(request.POST, request.FILES)
	if not form.is_valid():
		context = {
			'title': _('New post'),
			'post_days': (yesterday, datetime.date.today()),
			'form': form,
			'edit_post': edit_post,
		}

		return render_to_response('edit_post.html', context_instance=RequestContext(request, context))


	if not edit_post:
		# This is a new post, save it
		post = form.save(commit = False)

		if Post.objects.filter(author = request.user, date = post.date).count() > 0:
			return HttpResponse('Sorry, you already have an entry for that day')

		post.author = request.user
		post.save()
	else:
		# This is an edit of an existing post
		edit_post.text = form.cleaned_data['text']		
		edit_post.mood = form.cleaned_data['mood']	
		edit_post.save()	

	return HttpResponseRedirect('/')

@login_required
def show_post(request, post_id):
	post = get_object_or_404(Post, id = post_id, author = request.user)

	context = {
		'title': _('Your post #{}').format(post.get_user_id()),
		'post': post,
	}
	return render_to_response('show_post.html', context_instance=RequestContext(request, context))

def switch_language(request, language):
	request.session['django_language'] = language
	return HttpResponseRedirect('/')


def sign_up(request):
	if not request.method == 'POST':
		context = {
			'title': _('Sign up'),
		}

		return render_to_response('sign_up.html', context_instance=RequestContext(request, context))

	# Request method is POST
	form = SignUpForm(request.POST, request.FILES)
	if not form.is_valid():
		context = {
			'title': _('Sign up'),
			'form': form,
		}
		return render_to_response('sign_up.html', context_instance=RequestContext(request, context))

	# Check invite code
	try:
		invite = Invite.objects.get(code = request.POST.get('invite_code', None))
	except Invite.DoesNotExist:
		context = {
			'title': _('Sign up'),
			'form': form,
			'noinvite': True,
		}
		return render_to_response('sign_up.html', context_instance=RequestContext(request, context))

	# Fixme
	user = form.save(commit = False)
	user.set_password(request.POST.get('password', None))
	user.save()

	user.userprofile.public = request.POST.get('public', False)
	user.userprofile.invited_by = invite.generated_by
	user.userprofile.save()

	invite.delete()

	user.get_profile().send_verification_mail()

	login_user = django.contrib.auth.authenticate(username = user.username, password = request.POST.get('password', None))
	django.contrib.auth.login(request, login_user)
	return HttpResponseRedirect('/')



def login(request):
	if not request.method == 'POST':
		context = {
			'title': _('Login'),
		}
		return render_to_response('login.html', context_instance=RequestContext(request, context))

	# Request method is POST
	username = request.POST['username']
	password = request.POST['password']

	user = django.contrib.auth.authenticate(username = username, password = password)
	if user is not None and user.is_active:
		django.contrib.auth.login(request, user)
		user.get_profile().last_login_at = datetime.datetime.now()
		user.get_profile().save()
		return HttpResponseRedirect('/')

	context = {
		'title': _('Login'),
		'errors': True,
	}
	return render_to_response('login.html', context_instance = RequestContext(request, context))

def mail_verify(request, user_id, hash):
	user = get_object_or_404(User, id = user_id)
	profile = user.get_profile()

	if not hash == profile.get_verification_hash():
		return HttpResponse('Sorry, invalid hash.')

	profile.mail_verified = True
	profile.save()
	return HttpResponseRedirect("/")


def account_settings(request):
	if not request.method == 'POST':
		context = {
			'title': _('Account settings'),
			'form': AccountSettingsForm(),
		}
		return render_to_response('account_settings.html', context_instance=RequestContext(request, context))

	# Request method is POST
	form = AccountSettingsForm(request.POST, request.FILES)

	if not form.is_valid():
		context = {
			'title': _('Account settings'),
			'form': form,
		}
		return render_to_response('account_settings.html', context_instance=RequestContext(request, context))

	# Save form
	profile = request.user.get_profile()

	if request.user.email != form.cleaned_data['email']:
		profile.mail_verified = False
		request.user.email = form.cleaned_data['email']
		profile.send_verification_mail()

	profile.public = form.cleaned_data['public']

	profile.save()
	request.user.save()

	context = {
		'title': _('Account settings'),
		'success': True,
	}
	return render_to_response('account_settings.html', context_instance=RequestContext(request, context))

@api_view(['DELETE'])
def delete_post(request, post_id):
	"""
	Delete a post. This is currently an AJAX only view
	"""

	post = get_object_or_404(Post,
		id = post_id,
		author = request.user,
	)

	if not post.is_editable():
		raise PermissionDenied

	post.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)
