from django.utils.translation import ugettext as _
from inviteman.models import Invite
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template, Context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import EmailMessage
import django.forms as forms
from inviteman.serializers import InviteRequestSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

class InviteForm(forms.Form):
	email = forms.EmailField(max_length = 200)
	message = forms.CharField(max_length = 200, required = False)

@login_required
def invite(request):
	context = {
		'title': 'Invite someone',
		'invites_left': request.user.get_profile().invites_left,
	}

	if not request.method == 'POST':
		return render_to_response('invite.html', context_instance=RequestContext(request, context))

	# Request method is POST
	form = InviteForm(request.POST, request.FILES)

	if not form.is_valid():
		context['form'] = form
		return render_to_response('invite.html', context_instance=RequestContext(request, context))

	# Check if user has enough invites left
	profile = request.user.get_profile()

	# Since you shouldn't be able to do this unless you do nasty stuff anyways,
	# no need for a pretty error page
	if profile.invites_left < 1:
		return HttpResponse('Sorry, you don\'t have any invites left.')

	mail_template = get_template('mails/invite_friend.txt')

	# Generate the invite
	invite = Invite(generated_by = request.user)
	invite.save()

	# Remove from invites_left field
	profile.invites_left -= 1
	context['invites_left'] = profile.invites_left
	profile.save()

	mail_context = Context({
		'user': request.user,
		'invite': invite,
		'message': form.cleaned_data['message']
	})

	mail = EmailMessage(
			_('You\'ve been invited to join shortdiary by {}').format(request.user.username),
			mail_template.render(mail_context),
			'shortdiary <team@shortdiary.me>',
			['{}'.format(form.cleaned_data['email'])],
		)
	mail.send()
	return render_to_response('invite.html', context_instance=RequestContext(request, context))



@api_view(['POST'])
def invite_request(request):
	"""
	Add new invite request using AJAX
	"""
	serializer = InviteRequestSerializer(data=request.DATA)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)