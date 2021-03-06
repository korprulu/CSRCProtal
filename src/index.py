from django.shortcuts import render_to_response
from model.Publish import Publish
from google.appengine.api import users


def mainPage(request):

    publishs = Publish.all().order('-publish_date')
    
    template_values = {'publishs': publishs}
                
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
        
    return render_to_response('index.html', template_values)

def about(request):
    
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
        
    return render_to_response('about.html', template_values)

#class MobileTest(webapp.RequestHandler):
#    
#    def get(self):
#        self.response.out.write(self.request)
#
#class Test(webapp.RequestHandler):
#    
#    def get(self):
#        seq1 = ()
#        seq2 = []
#        
#        strArr = ['a','b','c','d','e','f','g']
#        for i,j in enumerate(strArr):
#            seq1 += j,
#            tempArr = []
#            for x in range(i):
#                tempArr.append(strArr[x])
#            seq2.append(tempArr)
#            
#        template_values = {'obj': zip(seq1,seq2)}
#        
#        path = os.path.join(os.path.dirname(__file__), './templates/test2.html')
#        self.response.out.write(template.render(path, template_values))
#    
def neo_soa_erp(request):
    
    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
    
    return render_to_response('neo_soa_erp.html', template_values)