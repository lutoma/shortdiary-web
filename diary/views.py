# coding: utf-8
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from diary.models import Post
from django.forms import ModelForm

def index(request):
	if not request.user.is_authenticated():
		context = {
			'title': 'Home',
			'content': 'Ohai.'
		}
		return render_to_response('base.html', context_instance=RequestContext(request, context))

	context = {
		'title': 'Home',
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
			'title': 'New post',
			'today': datetime.date.today(),
			'yesterday': datetime.date.today() - datetime.timedelta(days=1),
			'form': PostForm()
		}

		return render_to_response('new_post.html', context_instance=RequestContext(request, context))

	# Request method is POST
	form = PostForm(request.POST, request.FILES)
	if not form.is_valid():
		return HttpResponse('Invalid data.')

	post = form.save(commit = False)
	post.author = request.user
	post.save()

	return HttpResponseRedirect('/')

@login_required
def show_post(request, post_id):
	post = get_object_or_404(Post, id = post_id, author = request.user)

	context = {
		'title': 'Post from {}'.format(post.date),
		'post': post,
	}
	return render_to_response('show_post.html', context_instance=RequestContext(request, context))
