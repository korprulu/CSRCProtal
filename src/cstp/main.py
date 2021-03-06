'''
Created on 2011/3/18

@author: korprulu
'''
from google.appengine.api import users
from django.shortcuts import render_to_response, redirect
import re

def introduction(request):
        
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
                  
    return render_to_response('cstp/introduction.html', template_values)

def features(request):
        
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
                  
    return render_to_response('cstp/features.html', template_values)

def courses(request):
        
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
         
    return render_to_response('cstp/courses.html', template_values)         
        
def applyProcess(request):
        
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')     
     
    return render_to_response('cstp/applyprocess.html', template_values)                    

def admission(request):
    
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
        
    return render_to_response('cstp/admission.html', template_values)    

def download(self):
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
    
    return render_to_response('cstp/download.html', template_values)

def cstp(request):
    pattern = '.*(symbian|smartphone|midp|wap|phone|pda|mobile|mini|palm|netfront|android|bada).*'
    prog = re.compile(pattern, re.IGNORECASE)

    match = prog.search(str(request.META['HTTP_USER_AGENT']))
    if match:
        return redirect('/mobile/cstp')
    else:
        return redirect('/cstp/introduction')