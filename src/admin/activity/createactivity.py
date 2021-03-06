# -*- coding: utf-8 -*-
import os

from datetime import datetime, date, time
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from model.Activity import Activitydb

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        if users.get_current_user():
            template_values['userName'] = users.get_current_user().nickname().split('@')[0]
            template_values['logout'] = users.create_logout_url('/')

        path = os.path.join(os.path.dirname(__file__),'../../templates/admin/activity/createactivity.html')
        self.response.out.write(template.render(path, template_values))
              
class CreateActivity(webapp.RequestHandler):
    def post(self):
        activity = Activitydb()
        
        activity.activity_name = self.request.get('activity_name')
        activity.content = self.request.get('content')
        
        sign_start_Date = str(self.request.get('sign_StartDateTime')).split(" ")[0]
        sign_start_Time = str(self.request.get('sign_StartDateTime')).split(" ")[1]
        sign_end_Date = str(self.request.get('sign_EndDateTime')).split(" ")[0]
        sign_end_Time = str(self.request.get('sign_EndDateTime')).split(" ")[1]
        activity_start_Date = str(self.request.get('activity_StartDateTime')).split(" ")[0]
        activity_start_Time = str(self.request.get('activity_StartDateTime')).split(" ")[1]
        activity_end_Date = str(self.request.get('activity_EndDateTime')).split(" ")[0]
        activity_end_Time = str(self.request.get('activity_EndDateTime')).split(" ")[1]
        
        arr_sign_start_Date = str(sign_start_Date).split("-")
        arr_sign_start_Time = str(sign_start_Time).split(":")
        arr_sign_end_Date = str(sign_end_Date).split("-")
        arr_sign_end_Time = str(sign_end_Time).split(":")
        arr_activity_start_Date = str(activity_start_Date).split("-")
        arr_activity_start_Time = str(activity_start_Time).split(":")
        arr_activity_end_Date = str(activity_end_Date).split("-")
        arr_activity_end_Time = str(activity_end_Time).split(":")
        
        
        
        #input time formula: datetime.combine(Date,Time)
        #Date : date( int(Year),int(Month),int(Date) )   Time : time( int(hour),int(minute) )
        activity.sign_start = datetime.combine(date(int(arr_sign_start_Date[0]),int(arr_sign_start_Date[1]),int(arr_sign_start_Date[2])),time(int(arr_sign_start_Time[0]),int(arr_sign_start_Time[1]),int(arr_sign_start_Time[2])))
        activity.sign_end = datetime.combine(date(int(arr_sign_end_Date[0]),int(arr_sign_end_Date[1]),int(arr_sign_end_Date[2])),time(int(arr_sign_end_Time[0]),int(arr_sign_end_Time[1]),int(arr_sign_end_Time[2])))
        activity.activity_start = datetime.combine(date(int(arr_activity_start_Date[0]),int(arr_activity_start_Date[1]),int(arr_activity_start_Date[2])),time(int(arr_activity_start_Time[0]),int(arr_activity_start_Time[1]),int(arr_activity_start_Time[2])))
        activity.activity_end = datetime.combine(date(int(arr_activity_end_Date[0]),int(arr_activity_end_Date[1]),int(arr_activity_end_Date[2])),time(int(arr_activity_end_Time[0]),int(arr_activity_end_Time[1]),int(arr_activity_end_Time[2])))
        activity.site = self.request.get('site')

        if self.request.get('limit_num') != "" :
            activity.limit_num = int(self.request.get('limit_num'))
        #activity.activity_id = int(self.request.get('activity_id'))
        searchinfo = db.GqlQuery("SELECT * FROM Activitydb ORDER BY activity_id DESC")  #排序為了取的活動最大編號
        search_result = searchinfo.get();
        
        
            
        if self.request.get('activity_id') != "" :
            activity.activity_id = int(self.request.get('activity_id')) #使用基本設定<目前只容許到10000>
        else:
            if search_result == None:
                activity.activity_id = 10000;#第一筆活動
            else:
                activity.activity_id = search_result.activity_id+1 #目前設定
        
        activity.put()
        self.redirect('/Sendmail/id_'+str(activity.activity_id)) #to send mail<must to modify>
        
application = webapp.WSGIApplication([('/CreateActivity/Main', MainPage),('/CreateActivity/GoCreate',CreateActivity)],debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
