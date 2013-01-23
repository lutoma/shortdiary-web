from inviteman.models import Invite
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

@login_required
def invite(request):
	invite = Invite(generated_by = request.user)
	invite.save()

	context = {
		'title': 'Home',
		'content': 'Generated invite code: {}'.format(invite.code)
	}
	return render_to_response('base.html', context_instance=RequestContext(request, context))
