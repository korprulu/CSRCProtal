# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from model.WorkingHours import WorkingHours
from model.Employee import Employee
from google.appengine.api import users
from google.appengine.ext import db
import sys
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
import re
type = sys.getfilesystemencoding()
import time, datetime

def employeeList(request):

    employee = Employee.all()
        
    year = datetime.date.today().year
    month = datetime.date.today().month
    nextMonth = (month + 1) if month < 12 else 1
        
    time_format = "%Y-%m-%d"        
    
    bday = str(year) + "-" + str(month) + "-1"
    endday = str(year) + "-" + str(nextMonth) + "-1"                       
    sdate = datetime.date.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
    endate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
    working_hours = WorkingHours.gql("WHERE working_date >= :1 AND working_date < :2" \
                                , sdate, endate)
        
    seq1 = ()#key值陣列
    seq2 = []#時數
    for em in employee:
#        print em.mail
        seq1 += em.id,#設key id
        seq2.append(0)#放初值
        
    d = dict(zip(seq1,seq2))
    for work in working_hours:
        for i in employee:
            if work.worker == i.mail:
                d[int(i.id)] +=  work.subtotal

    # d.values is work subtotal
    personal_data = zip(d.values(),employee)

    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')    
    template_values['personal_data'] =  personal_data      
        
    return render_to_response('admin/employee/admin_employee.html', template_values)    

def Delete_Record(request):
  
        delete_id = request.POST['delete_id']
        worker = request.POST['worker']
        
        results = WorkingHours.gql("WHERE id = :1", int(delete_id))        
        for result in results:
            result.delete()
        return redirect('/admin/employee/show_workinghours/'+worker)


class Update_Record(webapp.RequestHandler):
    def post(self):
        """
        ifupdate = self.request.get('update')              
        if ifupdate=='true':
            id = self.request.get('id')  
            q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(id))
            results = q.fetch(10)
            for data in results:
                data.title = self.request.get('new_title')
                data.content = self.request.get('new_content')
                data.type = self.request.get('new_type')

                timestring = "2005-09-01"
                time_format = "%Y-%m-%d"
                                
                data.publish_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.request.get('new_date'), time_format)))
                #data.publish_date = self.request.get('new_date')
            db.put(results)
            self.redirect('/admin')        
        else :       
            update_title = self.request.get('update_id')
            q = db.GqlQuery("SELECT * FROM Publish WHERE id = :1", int(update_title))
            results = q.fetch(10)
    
            template_values = {'publishs': results}
              
            path = os.path.join(os.path.dirname(__file__), '../../templates/updatepublish.html')
            self.response.out.write(template.render(path, template_values))
        """

def addEmployee(request):

    result = Employee.gql('ORDER BY id DESC').get()

    employee = Employee()            
    employee.id = (result.id + 1) if result else 0  
    employee.name = request.POST['name']
    employee.mail = users.User(request.POST['mail'])
    employee.hourly_pay = int(request.POST['hourly_pay'])
    employee.put()
    #self.response.out.write(self.request.get('mail'))
    return redirect('/admin/employee')
        
def deleteEmployee(request):

    q = Employee.gql("WHERE id = :1", int(request.POST['id']))
    for result in q:
        result.delete()
        
    return redirect('/admin/employee')

def editEmployee(request):
               
    q = Employee.gql("WHERE id = :1", int(request.POST['id']))
    results = q.fetch(10)  
    template_values = {}  
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/') 
    template_values['employee'] = results
    return render_to_response('admin/employee/update_employee.html', template_values)
        
def updateEmployee(request):

    q = Employee.gql("WHERE id = :1", int(request.POST['id']))
    results = q.fetch(10)
    for data in results:
        data.name = request.POST['new_name']
#            data.mail = users.User(self.request.get('new_mail')+'@gmail.com')
        data.hourly_pay = int(request.POST['new_pay'])

    db.put(results)
    return redirect('/admin/employee')

def showWorkingHours(request, worker_mail):
    
    pattern = '([\w.]+)@([\w.]+)'
    regu = re.compile(pattern, re.IGNORECASE)
    
    if not regu.search(worker_mail): return redirect('/admin/employee')
    
    now = datetime.datetime.now()
    nowy=[]
    for i in range(5):
        nowy.append(now.year-i)
    mon=[1,2,3,4,5,6,7,8,9,10,11,12]
#    user = users.User(worker_mail+'@gmail.com')
    user = users.User(worker_mail)
    em_query = Employee.gql("WHERE mail = :1", user)        
    em_data = em_query.fetch(1)
    working_hours = WorkingHours.gql("WHERE worker = :1", user)        
 
    total_hour = 0
    total_pay = 0
    for work in working_hours:
        total_hour += work.subtotal
        total_pay += work.pay

    template_values = {}
    if users.get_current_user():
        template_values['userName'] = users.get_current_user().nickname().split('@')[0]
        template_values['logout'] = users.create_logout_url('/')
        template_values['em_data'] = em_data  
        template_values['working_hours'] = working_hours
        template_values['total_hour'] = total_hour
        template_values['total_pay'] = total_pay
        template_values['nowy'] = nowy
        template_values['mon'] = mon  
    try:
        em_mail = str(em_data.__getitem__(0).mail)
        template_values['em_mail'] = worker_mail#em_mail
        return render_to_response('admin/employee/browse_employee.html', template_values)
    except:               
        return HttpResponse('找不到此人的資料。')


def showMonthRecord(request, em_mail, year, month):

#    user = users.get_current_user()
    user = users.User(em_mail)
    time_format = "%Y-%m-%d"
    bday = year + "-" + month + "-" + '1'
    endday = year +"-" + unicode(int(month) + 1) + "-" + '1'
    sdate = datetime.date.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
    sdate2 = datetime.date.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
    em_data = Employee.gql("WHERE mail = :1", user)
    working_hours = WorkingHours.gql("WHERE worker = :1 AND working_date >= :2 AND working_date < :3",
                                      user, sdate, sdate2)
    total_hour = 0
    total_pay = 0
    for work in working_hours:
        total_hour += work.subtotal
        total_pay += work.pay
        
    if user:
        template_values = {'userName': users.get_current_user().nickname().split('@')[0],
                           'logout': users.create_logout_url('/'),
                           'em_data': em_data,
                           'working_hours': working_hours,
                           'total_hour': total_hour,
                           'total_pay': total_pay,
                           'select_year': year,
                           'select_month': month,
                           'em_mail': user.email()
                           }

    return render_to_response('admin/employee/browse_employee.html', template_values)
  
def printWorkingHours(request, em_mail, year, month):

#    user = users.get_current_user()
    user = users.User(em_mail)
    em_data = Employee.gql("WHERE mail = :1", user).fetch(1)

    time_format = "%Y-%m-%d"
    try:
        bday = year + '-' + month + '-1'
        endday = year + '-' + unicode(int(month) + 1) + "-1"
        sdate = datetime.date.fromtimestamp(time.mktime(time.strptime(bday, time_format)))
        sdate2 = datetime.date.fromtimestamp(time.mktime(time.strptime(endday, time_format)))
        working_hours = WorkingHours.gql("WHERE worker = :1 AND working_date >= :2 AND working_date < :3",
                                         user, sdate, sdate2)

        template_values = {'working_hours': working_hours,
                               'em_data':em_data}
            
        return render_to_response('table.html', template_values)
    except:
        return HttpResponse("請先選擇月份，初始畫面是所有的工讀紀錄。")

#application = webapp.WSGIApplication([('/admin/employee', MainPage),                                      
#                                      ('/employee/add_record', Add_Record),
#                                      ('/employee/delete_record', Delete_Record),
#                                      ('/employee/update_record', Update_Record),
#                                      ('/employee/add_employee', Add_Employee),
#                                      ('/employee/delete_employee/(.*)', Delete_Employee),
#                                      ('/employee/update_employee/(.*)', Update_Employee),
#                                      ('/employee/edit_employee/(.*)', Edit_Employee),
#                                      ('/employee/show_workinghours/(.*)', Show_WorkingHours),
#                                      ('/employee/', Personal_Record),
#                                      ('/employee/print_workinghours/',Print_WorkingHours),                           
#                                      ('/employee/show_monthrecord/', Show_Month_Record)], debug=True)        
#        