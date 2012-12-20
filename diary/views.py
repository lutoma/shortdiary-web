# coding: utf-8
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth
from diary.models import Post, Invite
from django.forms import ModelForm

tos = lambda request: render_to_response(
		'tos.html',
		context_instance = RequestContext(request, {'title': _('Terms of service')}),
	)

def index(request):
	try:
		randompost = Post.objects.filter(author__userprofile__public = True).order_by('?')[:1].get()
	except Post.DoesNotExist:
		randompost = None

	if not request.user.is_authenticated():
		context = {
			'title': _('Welcome to shortdiary'),
			'post': randompost,
		}
		return render_to_response('frontpage.html', context_instance=RequestContext(request, context))

	context = {
		'title': 'Home',
		'randompost': randompost,
		'posts': Post.objects.filter(author = request.user).order_by('-date', '-created_at')[:20],
	}
	return render_to_response('index.html', context_instance=RequestContext(request, context))

class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ('text', 'mood', 'date', 'image')

@login_required
def new_post(request):
	if not request.method == 'POST':
		context = {
			'title': _('New post'),
			'today': datetime.date.today(),
			'yesterday': datetime.date.today() - datetime.timedelta(days=1),
			'form': PostForm()
		}

		return render_to_response('new_post.html', context_instance=RequestContext(request, context))

	# Request method is POST
	form = PostForm(request.POST, request.FILES)
	if not form.is_valid():
		context = {
			'title': _('New post'),
			'today': datetime.date.today(),
			'yesterday': datetime.date.today() - datetime.timedelta(days=1),
			'form': form,
		}

		return render_to_response('new_post.html', context_instance=RequestContext(request, context))


	post = form.save(commit = False)

	if Post.objects.filter(author = request.user, date = post.date).count() > 0:
		return HttpResponse('Sorry, you already have an entry for that day')

	post.author = request.user
	post.save()

	return HttpResponseRedirect('/')

@login_required
def show_post(request, post_id):
	post = get_object_or_404(Post, id = post_id, author = request.user)

	context = {
		'title': _('Post from {0}').format(post.date),
		'post': post,
	}
	return render_to_response('show_post.html', context_instance=RequestContext(request, context))

def switch_language(request, language):
	request.session['django_language'] = language
	return HttpResponseRedirect('/')

class SignUpForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

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

	login_user = django.contrib.auth.authenticate(username = user.username, password = request.POST.get('password', None))
	django.contrib.auth.login(request, login_user)
	return HttpResponseRedirect('/')

@login_required
def invite(request):
	invite = Invite(generated_by = request.user)
	invite.save()

	context = {
		'title': 'Home',
		'content': 'Generated invite code: {}'.format(invite.code)
	}
	return render_to_response('base.html', context_instance=RequestContext(request, context))
