# -*- coding: utf-8 -*-

from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model.Activity import Activitydb
from model.Mail import Maildb

class MainPage(webapp.RequestHandler):
    def get(self):
        getActivityId = int(str(self.request.url).split('/Sendmail/id_')[1])
        searchActivityInfos = Activitydb.gql("WHERE activity_id = :1",getActivityId)
        searchActivityInfo = searchActivityInfos.get()
        
        searchMailInfos = Maildb.all()  #get activity info.
        for searchinfo in searchMailInfos:
            name = searchinfo.name
            activity_name = searchActivityInfo.activity_name
            sign_start = str(searchActivityInfo.sign_start)
            sign_end = str(searchActivityInfo.sign_end)
            activity_start = str(searchActivityInfo.activity_start)
            activity_end = str(searchActivityInfo.activity_end)
            mail.send_mail(sender="f210686@gmail.com", #use admin mail
                           to=searchinfo.mail,
                           subject=u"[活動通知]"+activity_name+u"~ 準備開跑嚕！",
                           body=
                                name+ u" ，您好："+"\n\n"
                                u"本團隊預定在 "+activity_start+u"將舉辦『" +activity_name + u"』活動"+ "\n"
                                u"報名的時間從 "+sign_start+ u"開放網路報名，" + "\n"
                                u"由於名額有限，若有意願想參加，請儘速進入活動網頁報名。" + "\n\n"
                                u"\t詳細活動時間： "+ activity_start + " ~ " + activity_end + "\n"
                                u"\t詳細報名時間："+ sign_start+ " ~ " +sign_end+"\n\n"
                                u"竭誠邀請您的參與\n\n輔大雲端服務中心 敬上\n\nhttp://xxxx.com" 
                            )
        self.redirect('/admin')
        
application = webapp.WSGIApplication([('/Sendmail/.*', MainPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()