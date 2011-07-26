'''
Created on 2011/3/17

@author: korprulu
'''
from django.shortcuts import render_to_response, redirect

    
def introduction(request):    
    return render_to_response('mobile/cstp/introduction.html')

def features(request):
    return render_to_response('mobile/cstp/features.html')
   
def courses(request):
    return render_to_response('mobile/cstp/courses.html')
    
def rules(request):
    return render_to_response('mobile/cstp/rules.html')
   
def admission(request):
    return render_to_response('mobile/cstp/admission.html')
    
def cstp(request):
    return redirect('/mobile/cstp/introduction')