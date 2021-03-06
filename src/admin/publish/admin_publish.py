#!/bin/python
# -*- coding: utf-8 -*-
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.Publish import Publish
from google.appengine.ext import db
from django.shortcuts import render_to_response, redirect
import sys
type = sys.getfilesystemencoding()
import time, datetime
from google.appengine.api import users

def publishList(request):
     
    publishs = Publish.all().order('-publish_date')
    template_values = {'publishs': publishs,
                       'userName': users.get_current_user().nickname().split('@')[0],
                       'logout': users.create_logout_url('/')}
                  
    return render_to_response('admin/publish/publish.html', template_values)    
  
def insert_Publish(request):
                
    publish = Publish.gql('ORDER BY id DESC').get()
    max = (publish.id + 1) if publish else 0
            
    bulletin = Publish()            
    bulletin.title = request.POST['title']
    bulletin.content = request.POST['content']
    bulletin.type = request.POST['type']
    bulletin.id = max + 1
#    bulletin.publish_date = datetime.datetime.now(TaiwanTimeZone())
    bulletin.put()
    
    return redirect('/admin/publish')
#        self.redirect('/admin/publish')


class Delete_Publish(webapp.RequestHandler):
    def post(self, delete_id):
        
        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(delete_id))
        results = q.fetch(10)
        for result in results:
            result.delete()
            
        self.redirect('/admin/publish')
        
class Edit_Publish(webapp.RequestHandler):
    def post(self, update_id):
               
        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(update_id))
        results = q.fetch(10)
    
        template_values = {'publishs': results,
                            'userName': users.get_current_user().nickname().split('@')[0],
                            'logout': users.create_logout_url('/')}
            
        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/publish/updatepublish.html')
        self.response.out.write(template.render(path, template_values))
        
class Update_Publish(webapp.RequestHandler):
    def post(self, update_id):
        
        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(update_id))
        results = q.fetch(10)
        for data in results:
            data.title = self.request.get('new_title')
            data.content = self.request.get('new_content')
            data.type = self.request.get('new_type')

            time_format = "%Y-%m-%d"                             
            data.publish_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.request.get('new_date'), time_format)))
            #data.publish_date = self.request.get('new_date')
        db.put(results)
        self.redirect('/admin/publish')

class Publish_Detail(webapp.RequestHandler):
    def get(self, looking_id):

        q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1 ", int(looking_id))        
        results = q.fetch(10)
                       
        template_values = {'publishs': results,
                           'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/')}
    
        path = os.path.join(os.path.dirname(__file__), '../../templates/admin/publish/publish_detail.html')
        self.response.out.write(template.render(path, template_values))

#application = webapp.WSGIApplication([('/admin/publish', MainPage),                                      
#                                      ('/publish/insert_publish', Insert_Publish),
#                                      ('/publish/delete_publish/(.*)', Delete_Publish),
#                                      ('/publish/edit_publish/(.*)', Edit_Publish),
#                                      ('/publish/update_publish/(.*)', Update_Publish),                      
#                                      ('/publish/publish_detail/(.*)',Publish_Detail)], debug=False)        
#        
#def main():
#    run_wsgi_app(application)
#    
#if __name__ == "__main__":
#    main()
