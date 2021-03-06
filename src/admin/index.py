from google.appengine.api import users
from django.shortcuts import render_to_response

def mainPage(request):
        
    user = users.get_current_user()

    template_values = {}

    if user:
        template_values['userName'] = user.nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
        
    return render_to_response('admin/index.html', template_values)                        