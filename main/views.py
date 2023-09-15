
import os
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . models import *
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from BruteBuster .models import FailedAttempt 
from django.db.models import Sum
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.core.mail import send_mail
import datetime as d
import xlwt





def change_pass_page(request):
    users = User.objects.all()
    return render(request, 'main/change_pass_page.html' ,{'users':users})

def change_pass(request,id):

    user = User.objects.get(id=id)
    
    if request.POST['passwords'] != '' and request.POST['newpassconf'] != '':
            
            if request.POST['passwords'] == request.POST['newpassconf']:
                user.set_password(request.POST['newpassconf'])
           
                return HttpResponseRedirect(reverse('login'))
    context = {'user':user}
    return render(request,'main/change_pass_page.html',context)

        
    

def mail_send(request):
    if request.method =='POST':
        # msg = request.POST['messages']
        # name = request.POST['name']
        email = request.POST['email']
        # sbjct = request.POST['subject']

        # subject= request.POST['name'], request.POST['subject'], request.POST['email']  
        message   =  'http://127.0.0.1:8000/mail_send/' 
        email_from = settings.EMAIL_HOST_USER
        qebul_eden = [email,]
        # qebul = ["horadiztorpag2017@gmail.com",]
        
        send_mail('',message,email_from,qebul_eden)
        
        # send_mail(subject, msg, email_from, qebul)
    return render(request,'main/mail_send.html')


def axes_lockout(request):
    return render(request , 'main/axes_lockout.html')

def todoapp(request):
    img = 0
    if Profil.objects.filter(user_id_id=request.user.id).exists(): 
        img = Profil.objects.filter(user_id_id=request.user.id) 
    if request.method=='POST' and 'sorgu' in request.POST:
        x = request.POST['sorgu']
        info = Tapsiriq.objects.filter(Q(tapsiriq__contains=x)).filter(user_id_id=request.user.id).order_by('-id')
        say = Tapsiriq.objects.filter(Q(tapsiriq__contains=x)).count()
    else:    
        info =  Tapsiriq.objects.filter(user_id_id=request.user.id).order_by('-id')
        say =  Tapsiriq.objects.filter(user_id_id=request.user.id).count()    
    say1 = 0
    say2 = 0
    for x in info:
        if x.qalanvaxt == 0:
            say2+=1
        else:
            say1+=1    
    if request.method=="POST" and 'l' in request.POST:
        a = request.POST['tapsiriq']
        b = request.POST['tarix']
        c = request.POST['saat']
        if a=='' or b=='' or c=='':
            messages.info(request,'Melumatlar tam deyil',extra_tags="warning")
        else:
            
            daxilet=Tapsiriq(tapsiriq=a,tarix=b,saat=c,user_id_id = request.user.id)
            daxilet.save() 
            return HttpResponseRedirect(reverse('todoapp'))

            
    data={'info':info,'say':say,'say1':say1,'say2':say2,'img':img}           
    return render(request,'main/todoapp.html',data)

def excel(request):
    response = HttpResponse(content_type='main/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Tapsiriq' + \
    str(d.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tapsiriq')
    row_num=0
    font_style = xlwt.XFStyle()
    columns = ['tapsiriq','tarix','saat']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()
    rows = Tapsiriq.objects.filter(user_id_id=request.user.id).values_list('tapsiriq','tarix','saat')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response






def deleteapp(request,id):
    foto = Profil.objects.get(user_id_id=request.user.id) 
    messages.info(request,"Melumati silmeye eminsiz?",extra_tags='primary')
    info = Tapsiriq.objects.filter(user_id_id=request.user.id).order_by('-id')
    say =  Tapsiriq.objects.filter(user_id_id=request.user.id).count()
    say1 = 0
    say2 = 0
    for x in info:
        if x.qalanvaxt == 0:
            say2+=1
        else:
            say1+=1  
    data={'info':info,'sil_id':id,'say':say,'say1':say1,'say2':say2,'foto':foto}
    return render(request,'main/todoapp.html',data)

def sil(request,id):
    info = Tapsiriq.objects.filter(id=id)
    info.delete()
    messages.info(request,"Bu melumat silindi",extra_tags='success')
    return HttpResponseRedirect(reverse('todoapp'))

def editapp(request,id):
    foto = Profil.objects.get(user_id_id=request.user.id) 
    info = Tapsiriq.objects.filter(user_id_id=request.user.id).order_by('-id')
    say =  Tapsiriq.objects.filter(user_id_id=request.user.id).count()
    say1 = 0
    say2 = 0
    for x in info:
        if x.qalanvaxt == 0:
            say2+=1
        else:
            say1+=1  
    edit = Tapsiriq.objects.get(id=id)
    data={'info':info,'edit':edit,'say':say,'say1':say1,'say2':say2,'foto':foto}
    return render(request,'main/todoapp.html',data)

def updateapp(request,id):
    info = Tapsiriq.objects.get(id=id)
    if request.method=="POST":
        b = d.datetime.now()
        z = d.datetime(b.date().year,b.date().month,b.date().day,b.time().hour,b.time().minute,b.time().second)
        a = request.POST['tapsiriq']
        b = request.POST['tarix']
        c = request.POST['saat']
    if a=='' or b=='' or c=='':
       messages.info(request,"Melumat tam deyil",extra_tags='warning')     
    else:
        info.tapsiriq = a
        info.tarix = b
        info.saat = c
        info.save()
        messages.info(request,"Melumat ugurla yenilendi",extra_tags='success')
    return HttpResponseRedirect(reverse('todoapp'))      

def secim(request,id):  
    foto = Profil.objects.filter(user_id_id=request.user.id) 
    if request.method=='POST' and 'sorgu' in request.POST:
        x = request.POST['sorgu']
        info = Tapsiriq.objects.filter(Q(tapsiriq__contains=x)).order_by('-id')
        say = Tapsiriq.objects.filter(Q(tapsiriq__contains=x)).count()
    else:    
        info =  Tapsiriq.objects.filter(user_id_id=request.user.id).order_by('-id')
        say =  Tapsiriq.objects.filter(user_id_id=request.user.id).count()    
    say1 = 0
    say2 = 0
    for x in info:
        if x.qalanvaxt == 0:
            say2+=1
        else:
            say1+=1    
    if request.method=="POST" and 'l' in request.POST:
        a = request.POST['tapsiriq']
        b = request.POST['tarix']
        c = request.POST['saat']
        if a=='' or b=='' or c=='':
            messages.info(request,'Melumatlar tam deyil',extra_tags="warning")
        else:
            daxilet=Tapsiriq(tapsiriq=a,tarix=b,saat=c)
            daxilet.save() 
    data={'info':info,'say':say,'say1':say1,'say2':say2,'foto':foto,'filter':id}           
    return render(request,'main/todoapp.html',data)

#Error page -----

def error_404(request, exception):
    img = Profil.objects.filter(user_id_id = request.user.id)

    data = {'img':img}
    return render(request,'404.html', data)


def error_403(request,  exception):
        data = {}
        return render(request,'500.html', data)
def error_400(request,  exception):
        data = {}
        return render(request,'500.html', data)


def deluserconfirm(request,id):
    
    deluser = User.objects.get(id=request.user.id)
    userid = User.objects.filter(id=request.user.id)
    profil = User.objects.filter(id=request.user.id)
    edit = User.objects.get(id=request.user.id)
    return render(request, 'main/profile.html',{'profil':profil,'edit':edit,'userid':userid,'deluser':deluser})
def deleteuser(request,id):
    delus = User.objects.get(id=request.user.id)
    delus.delete()
    return render(request,'main/login.html')
#Profile ----
@login_required
def profile(request):
    userid = User.objects.filter(id = request.user.id)
    profil = User.objects.filter(id=request.user.id)
    editimg = User.objects.get(id=request.user.id)
    img = Profil.objects.filter(user_id_id = request.user.id)
    return render(request, 'main/profile.html',{'profil':profil,'editimg':editimg,'userid':userid,'img':img})

def updateprofile(request,id):
    
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    newpassconf = request.POST['newpassconf']
    user = User.objects.get(id=id)
    if user.check_password(password):
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        profile= Profil.objects.filter(user_id_id = request.user.id).count()
        if profile == 0 :
            # foto = Profil.objects.get(user_id_id = request.user.id)
            if request.method=='POST' and  'foto' in request.FILES:
                foto=request.FILES['foto']
                fs = FileSystemStorage()
                filename=fs.save(foto.name,foto)
                uploaded_file_url=fs.url(filename)
                daxilet = Profil(foto = uploaded_file_url,user_id_id=request.user.id)
                daxilet.save()
            
        
        else:
            

            if request.method=='POST' and  'foto' in request.FILES:
                foto=request.FILES['foto']
                fs = FileSystemStorage()
                filename=fs.save(foto.name,foto)
                uploaded_file_url=fs.url(filename)
                f = Profil.objects.get(user_id_id=request.user.id)
                f.foto = uploaded_file_url
                
                f.save()
    
    else:
        messages.warning(request,'Xahis Edirik Cari Parolu Daxil Edin')
    
    if user.check_password(password):
        
        if newpassconf != '' and request.POST['newpass'] != '':
            
            if request.POST['newpass']==newpassconf:
                user.set_password(request.POST['newpass'])
            else:
                messages.warning(request,'Parollar uygun deyil')
        # else:
        #     messages.warning(request,'Ugurlu')
   
    user.save()
        
    # user.password = password

    return HttpResponseRedirect(reverse('profile'))

#  Admin -------
def users(request):
    
        img = Profil.objects.filter(user_id_id = request.user.id)

        
        return render(request,'main/users.html' , {'img':img}  )

def ajaxusers(request):
    section = 'users'
    entry_list = User.objects.all()
    
    if 'sil_user' in request.GET:
        user=User.objects.get(id=request.GET['sil_user'])
        user.delete()
        return HttpResponseRedirect(reverse('users'))
        
    return render(request,'main/loader.html' , {'entry_list':entry_list,'section':section})



def block_user(request,id):
    user = User.objects.get(id=id)

    
    user.is_active = 0
    user.save()
    
    return HttpResponseRedirect(reverse('users'))

def active_user(request,id):
    
    user = User.objects.get(id=id)
    
    user.is_active = 1
    user.save()
    
    return HttpResponseRedirect(reverse('users'))

# def delete_user(request):
    
#     if 'sil_user' in request.GET:F
#         user=User.objects.get(id=request.GET['sil_user'])
#         user.delete()
#         return HttpResponseRedirect(reverse('users'))
# Axtar -------
def axtar(request):
    x = request.POST['sorgu']
    my_brands=Brands.objects.filter(Q(Brand__contains=x) , Q(Tarix__contains = x) ).filter(id = request.user.id)

    template=loader.get_template('main/loader.html')
    data={'brands':my_brands,'x':x}
    return HttpResponse(template.render(data,request))

def clientsaxtar(request):
    x = request.POST['sorgu']
    myclients=Clients.objects.filter(Ad__contains=x)

    template=loader.get_template('main/loader.html')
    data={'x':x,'clients':myclients}
    return HttpResponse(template.render(data,request))


def axtarclient(request):
    x = request.POST['sorgu']
    searchcl=Clients.objects.filter(Q(Ad__contains=x), Q(Soyad__contains=x))
    template=loader.get_template('main/clients.html')
    data={'searchcl':searchcl,'x':x}
    return HttpResponse(template.render(data,request))

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Bu istifadeci artiq movcuddur')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Bu email artiq movcuddur')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('login')
        else:
            messages.info(request, 'Parollar uygun deyil')
            return redirect('register')
            
    else:
        return render(request, 'main/register.html')
    


def login(request): 
     
    # user_id = User.objects.get(id=id)
    # if user_id.is_active == 0:
    #     messages.info(request, 'block')
    #     return redirect('login')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password , request=request)
        # failed =FailedAttempt.objects.filter(username=request.user.username).aggregate(
        #     total_failures=Sum('failures'))['total_failures']
        
        # user_id = User.objects.get(id=request.user.id)
        # if user_id.is_active == 0:
        #     messages.info(request, 'block')
        #     return redirect('login')
        

        if user is not None:
                # if failed>3 :
                
                auth.login(request,user)
                return redirect('index')
                
                # else:
                #     messages.info(request,'Cix bayra')
                 
        else:
            
            messages.info(request, 'Login ve ya parol yanlishdir')
            return redirect('login')
        
    else:
        
        return render(request, 'main/login.html' )
    
# def block_user(request):
#     if request.user.is_active:
#         request.user.is_active= False
#     return HttpResponseRedirect(reverse('login'))
        
def logout(request):
    auth.logout(request)
    return redirect('index')





##################################### Brands ###########################################
def index(request):
   
    img = Profil.objects.filter(user_id_id = request.user.id)
    

    return render(request,'main/index.html',{'img':img})



def ajaxloader(request):
    section = 'brands'
    if request.POST.getlist('x[]'):    
        if request.method=='POST':
            for x in request.POST.getlist('x[]'):
                sil = Brands.objects.get(id=x)
                sil.delete()
        return HttpResponseRedirect(reverse('index'))
    
    if 'axtar' in request.POST:
        
        x = request.POST['sorgu']
        my_brands=Brands.objects.filter(Q(Brand__contains=x) , Q(user_id = request.user.id))
        data={'brands':my_brands,'x':x,'section':section}
        return render(request,'main/loader.html',data)

    if 'sil_id' in request.GET:
        yoxla= Mehsul.objects.filter(Brand_id_id=request.GET['sil_id']).count()
        if yoxla == 0 :
            if request.method=='GET':
                

                brand=Brands.objects.get(id=request.GET['sil_id'])
                image = str(settings.BASE_DIR) + str(brand.Foto)
                os.remove(image)

  
                brand.delete()
                messages.success(request,'Ugurla silindi') 
        else:
            messages.success(request,'Bu mehsul aktivdir')   
        return HttpResponseRedirect(reverse('index'))

    if 'brand_insert' in request.POST:
        
        if request.method=='POST' and request.FILES['foto']:
            if 'foto' in request.FILES:
                foto=request.FILES['foto']
                fs = FileSystemStorage()
                filename=fs.save(foto.name,foto)
                uploaded_file_url=fs.url(filename)
    
        
        x = request.POST['brand']

        bsay = Brands.objects.filter(Q(Brand = x) , Q(user_id = request.user.id)).count()

        if bsay==0:
            daxil_et = Brands(Brand=x,Foto=uploaded_file_url,user_id=request.user.id)
            daxil_et.save()
            messages.success(request, 'Brend uğurla əlavə edildi')
        else:
            messages.warning(request, 'Bu brend artıq mövcuddur')
                    
    
    if 'edit_id' in request.GET:
        
        info = Brands.objects.get(id=request.GET['edit_id'])
        my_brands=Brands.objects.filter(user_id=request.user.id).order_by('-id')
        bsay = Brands.objects.filter(user_id=request.user.id).count() 
        data={'brands':my_brands,'bsay':bsay,'edit':info,'section':section}
        return render(request ,'main/loader.html', data)
        
    if 'all_update' in request.POST:

        if request.method=='POST' and 'foto' in request.FILES:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)
        else:
            uploaded_file_url = request.POST['cari_foto']

        x = request.POST['brand']

        bsay = Brands.objects.filter(user_id=x).exclude(id=request.POST['id']).count()

        if bsay==0:
            yenile = Brands.objects.get(id=request.POST['id'])
            yenile.Brand = x
            yenile.Foto = uploaded_file_url
            yenile.save()
            messages.success(request, 'Brend uğurla yenilendi')
        else:
            messages.warning(request, 'Bu brend artıq mövcuddur')

    filter1 = ''
    
    img = Profil.objects.filter(user_id_id = request.user.id)
    my_brands=Brands.objects.filter(user_id=request.user.id).order_by('-id')

    if 'f1' in request.GET:
        if request.GET['f1']=='za':
            
            my_brands=Brands.objects.filter(user_id=request.user.id).order_by('Brand')
            filter1 = 'az'
        if request.GET['f1']=='az':
            my_brands=Brands.objects.filter(user_id=request.user.id).order_by('-Brand')
            filter1 = 'za'

    bsay = Brands.objects.filter(user_id=request.user.id).count()
    img = Profil.objects.filter(user_id_id = request.user.id)

    
    template=loader.get_template('main/loader.html')
    data={'brands':my_brands,'bsay':bsay,'img':img,'section':section,'filter1':filter1}

    return HttpResponse(template.render(data,request))

def delete_all(request):
    
    Brands.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))

def addbrand(request):

    if request.method=='POST' and request.FILES['foto'] and request.FILES['foto'] != '':
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)
    x = request.POST['brand']

    bsay = Brands.objects.filter(Q(Brand = x) , Q(user_id = request.user.id)).count()

    if bsay==0:
        daxil_et = Brands(Brand=x,Foto=uploaded_file_url,user_id=request.user.id)
        daxil_et.save()
        messages.success(request, 'Brend uğurla əlavə edildi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')
    
    return HttpResponseRedirect(reverse('index'))
    


def delete(request,id):
    yoxla= Mehsul.objects.filter(Brand_id_id=id).count()
    if yoxla == 0 :
        if request.method=='POST':
            brand=Brands.objects.get(id=id)       
            brand.delete()
            messages.success(request,'Ugurla silindi') 
    else:
        messages.success(request,'Bu mehsul aktivdir')   
    return HttpResponseRedirect(reverse('index'))


# def deleteconfirm(request,id):
   
#     my_brands=Brands.objects.filter(user_id=request.user.id).order_by('-id')
#     bsay = Brands.objects.filter(user_id=request.user.id).count() 
#     deleteconf = Brands.objects.get(id=id)
#     template=loader.get_template('main/index.html')
#     data={'brands':my_brands,'bsay':bsay,"deleteconf":deleteconf}
#     return HttpResponse(template.render(data,request))
    
def edit(request,id):
    info = Brands.objects.get(id=id)
    my_brands=Brands.objects.filter(user_id=request.user.id).order_by('-id')
    bsay = Brands.objects.filter(user_id=request.user.id).count() 
    template=loader.get_template('main/index.html')
    data={'brands':my_brands,'bsay':bsay,'edit':info}
    return HttpResponse(template.render(data,request))

def update(request, id):

    if request.method=='POST' and 'foto' in request.FILES:
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)
    else:
        uploaded_file_url = request.POST['cari_foto']

    x = request.POST['brand']


    bsay = Brands.objects.filter(user_id=x).exclude(id=id).count()

    if bsay==0:
        yenile = Brands.objects.get(id=id)
        yenile.Brand = x
        yenile.Foto = uploaded_file_url
        yenile.save()
        messages.success(request, 'Brend uğurla yenilendi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')

    
    return HttpResponseRedirect(reverse('index'))
# &&&& Clients

def clients(request):
    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/clients.html',{'img':img})

def ajaxclients(request):
    section = 'clients'
    if 'sil_id' in request.GET:
        sifaris_yoxla = Sifaris.objects.filter(Client_id_id=request.GET['sil_id']).count()

        if sifaris_yoxla == 0:
            if request.method=='GET':
                cl_id=Clients.objects.get(id=request.GET['sil_id'])
                image = str(settings.BASE_DIR) + str(cl_id.Foto)
                os.remove(image)
                cl_id.delete()
                messages.success(request,'Ugurla silindi')
        else:
            messages.warning(request,'Bu mehsul hal-hazirda aktivdir') 
            
        return HttpResponseRedirect(reverse('clients'))

    if 'clinsert' in request.POST:
        if request.method=='POST' and request.FILES['foto']:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)
    
        Ad=request.POST['ad']
        Soyad=request.POST['soyad']
        Tel=request.POST['tel']
        Email=request.POST['email']
        Sirket=request.POST['sirket']
        bsay = Clients.objects.filter(Ad=request.user.id,Soyad=request.user.id).count()

        if bsay==0:
            add = Clients(Ad=Ad,Soyad=Soyad,Tel=Tel,Foto=uploaded_file_url,Email=Email,Sirket=Sirket,user_id=request.user.id)
            add.save()
            messages.success(request, 'Brend uğurla əlavə edildi')
        else:
            messages.warning(request, 'Bu brend artıq mövcuddur')
    if 'edit_id' in request.GET:

        info=Clients.objects.get(id=request.GET['edit_id'])
        myclients=Clients.objects.filter(user_id=request.user.id).order_by('-id')
        bsay = Clients.objects.filter(user_id=request.user.id).count()
        template = loader.get_template('main/loader.html')
        data={'clients':myclients,"bsay":bsay,"editklient":info,'section':section}
        return render(request,'main/loader.html',data)

    if 'clupdate' in request.POST:
        if request.method=='POST' and 'foto' in request.FILES:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)
        else:
            uploaded_file_url = request.POST['cari_foto']
    
        Ad = request.POST['ad']
        Soyad = request.POST['soyad']
        Tel = request.POST['tel']
        # Foto = request.POST['foto']
        Email = request.POST['email']
        Sirket = request.POST['sirket']
        bsay = Clients.objects.filter(Ad=Ad).exclude(id=request.POST['id']).count()
        if bsay==0:
            yenile = Clients.objects.get(id=request.POST['id'])
            yenile.Ad = Ad
            yenile.Soyad = Soyad
            yenile.Tel = Tel
            yenile.Foto = uploaded_file_url
            yenile.Email = Email
            yenile.Sirket = Sirket
            yenile.save()
            messages.success(request, 'Brend uğurla yenilendi')
        else:
            messages.warning(request, 'Bu brend artıq mövcuddur')
    filter1 = ''
    if 'f1' in request.GET:
        if request.GET['f1']=='za':
            
            myclients=Clients.objects.filter(user_id=request.user.id).order_by('Ad')
            filter1 = 'az'
        if request.GET['f1']=='az':
            myclients=Clients.objects.filter(user_id=request.user.id).order_by('-Ad')
            filter1 = 'za'
    
    img = Profil.objects.filter(user_id = request.user.id)
    myclients=Clients.objects.filter(user_id=request.user.id).order_by('-id')
    bsay = Clients.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/loader.html')
    data={'clients':myclients,'bsay':bsay,'img':img,'section':section,'filter1':filter1}
    return HttpResponse(template.render(data,request))

def addclient(request):
    
    if request.method=='POST' and request.FILES['foto']:
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)
    
    Ad=request.POST['ad']
    Soyad=request.POST['soyad']
    Tel=request.POST['tel']
    Email=request.POST['email']
    Sirket=request.POST['sirket']
    bsay = Clients.objects.filter(Ad=request.user.id,Soyad=request.user.id).count()

    if bsay==0:
        add = Clients(Ad=Ad,Soyad=Soyad,Tel=Tel,Foto=uploaded_file_url,Email=Email,Sirket=Sirket,user_id=request.user.id)
        add.save()
        messages.success(request, 'Brend uğurla əlavə edildi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')
    

    return HttpResponseRedirect(reverse('clients'))
    
def deleteclient(request,id):
    sifaris_yoxla = Sifaris.objects.filter(Client_id_id=id).count()

    if sifaris_yoxla == 0:
        if request.method=='POST':
            cl_id=Clients.objects.get(id=id)
            cl_id.delete()
            messages.success(request,'Ugurla silindi')
    else:
        messages.warning(request,'Bu mehsul hal-hazirda aktivdir') 
    
   
    return HttpResponseRedirect(reverse('clients'))

# def deleteconfirmclient(request,id):
#     myclients=Clients.objects.filter(user_id=request.user.id).order_by('-id')
#     bsay = Clients.objects.filter(user_id=request.user.id).count()
#     clyoxla = Clients.objects.get(id=id)
#     template=loader.get_template('main/clients.html')
#     data={'clients':myclients,'bsay':bsay,"clyoxla":clyoxla}
#     return HttpResponse(template.render(data,request))

def updateclients(request,id):
    
    info=Clients.objects.get(id=id)
    myclients=Clients.objects.filter(user_id=request.user.id).order_by('-id')
    bsay = Clients.objects.filter(user_id=request.user.id).count()
    template = loader.get_template('main/clients.html')
    data={'clients':myclients,"bsay":bsay,"editklient":info}
    return HttpResponse(template.render(data,request))
  
def updaterecordclients(request, id):
    if request.method=='POST' and 'foto' in request.FILES:
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)
    else:
        uploaded_file_url = request.POST['cari_foto']
    Ad = request.POST['ad']
    Soyad = request.POST['soyad']
    Tel = request.POST['tel']
    # Foto = request.POST['foto']
    Email = request.POST['email']
    Sirket = request.POST['sirket']
    bsay = Clients.objects.filter(Ad=Ad).exclude(id=id).count()
    if bsay==0:
        yenile = Clients.objects.get(id=id)
        yenile.Ad = Ad
        yenile.Soyad = Soyad
        yenile.Tel = Tel
        yenile.Foto = uploaded_file_url
        yenile.Email = Email
        yenile.Sirket = Sirket
        yenile.save()
        messages.success(request, 'Brend uğurla yenilendi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')
    return HttpResponseRedirect(reverse('clients'))

# &&& Xercler

def xercler(request): 
    img = Profil.objects.filter(user_id_id = request.user.id)
 
    return render(request,'main/xercler.html',{'img':img})

def ajaxxercler(request):
    section = 'xercler'        

    if 'sil_id' in request.GET:
        xercler=Xercler.objects.get(id=request.GET['sil_id'])
        xercler.delete()
        return HttpResponseRedirect(reverse('xercler'))
    if 'xercinsert' in request.POST:
        Teyinat=request.POST['teyinat']
        Mebleg=request.POST['mebleg']
        bsay = Xercler.objects.filter(Teyinat=Teyinat).count()

        if bsay==0: 
            add=Xercler(Teyinat=Teyinat,Mebleg=Mebleg,user_id=request.user.id)
            add.save()
            messages.success(request, 'Brend uğurla əlavə edildi')
        else:
            messages.warning(request, 'Bu brend artıq mövcuddur')
    if 'edit_id' in request.GET:
        info = Xercler.objects.get(id=request.GET['edit_id'])
        myxercler=Xercler.objects.filter(user_id=request.user.id).order_by('-id')
        bsay = Xercler.objects.filter(user_id=request.user.id).count()
        data={'xercler':myxercler,'bsay':bsay,'edit':info,'section':section}
        return render(request,'main/loader.html' , data)
    if 'xercupdate' in request.POST:
        first = request.POST['teyinat']
        second = request.POST['mebleg']
        bsay = Xercler.objects.filter(Teyinat=first,Mebleg=second).exclude(id=request.POST['id']).count()

        if bsay==0:
            yenile = Xercler.objects.get(id=request.POST['id'])
            yenile.Teyinat = first
            yenile.Mebleg = second
            yenile.save()
            messages.success(request, 'Brend uğurla yenilendi')
        else:
            messages.warning(request, 'Bu brend artıq mövcuddur')
    myxercler=Xercler.objects.filter(user_id=request.user.id).order_by('-id')
    bsay = Xercler.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/loader.html')
    data={'xercler':myxercler,'bsay':bsay,'section':section}
    return HttpResponse(template.render(data,request))

def addxercler(request):
    Teyinat=request.POST['teyinat']
    Mebleg=request.POST['mebleg']
    bsay = Xercler.objects.filter(Teyinat=Teyinat).count()

    if bsay==0: 
        add=Xercler(Teyinat=Teyinat,Mebleg=Mebleg,user_id=request.user.id)
        add.save()
        messages.success(request, 'Brend uğurla əlavə edildi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')
    return HttpResponseRedirect(reverse('xercler'))
def deletexercler(request,id):
    xercler=Xercler.objects.get(id=id)
    xercler.delete()
    return HttpResponseRedirect(reverse('xercler'))
def updatexercler(request,id):
    info = Xercler.objects.get(id=id)
    myxercler=Xercler.objects.filter(user_id=request.user.id).order_by('-id')
    bsay = Xercler.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/xercler.html')
    data={'xercler':myxercler,'bsay':bsay,'edit':info}
    return HttpResponse(template.render(data,request))
   
def updaterecordxercler(request, id):
    first = request.POST['teyinat']
    second = request.POST['mebleg']
    bsay = Xercler.objects.filter(Teyinat=first,Mebleg=second).exclude(id=id).count()

    if bsay==0:
        yenile = Xercler.objects.get(id=id)
        yenile.Teyinat = first
        yenile.Mebleg = second
        yenile.save()
        messages.success(request, 'Brend uğurla yenilendi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')
    return HttpResponseRedirect(reverse('xercler'))
# Mehsul  

def mehsul(request): 
    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/mehsul.html',{'img':img})

def ajaxmehsul(request):
    section = 'mehsuls'
    if 'sil_id' in request.GET:
         
        sifaris_yoxla = Sifaris.objects.filter(Mehsul_id_id=request.GET['sil_id']).count()

        if sifaris_yoxla == 0:
            meh_id=Mehsul.objects.get(id=request.GET['sil_id'])
            image = str(settings.BASE_DIR) + str(meh_id.Foto)
            os.remove(image)
            meh_id.delete()
            messages.success(request,'Ugurla silindi')
        else:
            messages.warning(request,'Bu mehsul hal-hazirda aktivdir') 
        return HttpResponseRedirect(reverse('mehsul'))


    if 'mehsulinsert' in request.POST:
        if request.method=='POST' and request.FILES['foto']:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)

        Brand_id = request.POST['brand']
        Ad = request.POST['ad']
        Alish = request.POST['alish']
        Satish = request.POST['satish']
        Miqdar = request.POST['miqdar']
        bsay = Mehsul.objects.filter(Brand_id=request.user.id,Ad=request.user.id).count()

        if bsay==0: 
            r=Brands.objects.get(id=Brand_id)
            add= Mehsul(Brand_id=r,Foto=uploaded_file_url,Ad=Ad,Alish=Alish,Satish=Satish,Miqdar=Miqdar,user_id=request.user.id)
            add.save()
            messages.success(request, 'Mehsul anbara uğurla əlavə edildi')
        else:
            messages.warning(request, 'Bu Mehsul artıq mövcuddur')
    
    if 'edit_id' in request.GET:
        info = Mehsul.objects.get(id=request.GET['edit_id'])
        mehsul = Mehsul.objects.filter(user_id=request.user.id).order_by('-id')
        bsay = Mehsul.objects.filter(user_id=request.user.id).count()
        my_brands=Brands.objects.filter(user_id=request.user.id)
        data={'mehsul':mehsul,'bsay':bsay,'editmehsul':info,'my_brands':my_brands,'section':section}
        return render(request,'main/loader.html',data)

    if 'mehsulupdate' in request.POST:
        if request.method=='POST' and 'foto' in request.FILES:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)
        else:
            uploaded_file_url = request.POST['cari_mehsul']
        
                
        Brand_id = request.POST['brand']
        Ad = request.POST['ad']
        Alish = request.POST['alish']
        Satish = request.POST['satish']
        Miqdar = request.POST['miqdar']
    

        meh = Mehsul.objects.get(id = request.POST['id'])
        r = Brands.objects.get(id = meh.Brand_id_id)
        member = Mehsul.objects.get(id=request.POST['id'])
        member.Brand_id = r
        member.Ad = Ad
        member.Foto = uploaded_file_url
        member.Alish = Alish
        member.Satish = Satish
        member.Miqdar = Miqdar
        member.save()
        messages.success(request, 'Brend uğurla yenilendi')

    
    mehsul=Mehsul.objects.filter(user_id=request.user.id).select_related().order_by('-id')
    my_brands=Brands.objects.filter(user_id=request.user.id)
    bsay = Mehsul.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/loader.html')
    data = {'mehsul': mehsul,'my_brands':my_brands,"bsay":bsay,'section':section}
    return HttpResponse(template.render(data,request))

def addmehsul(request):
    if request.method=='POST' and request.FILES['foto']:
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)

    Brand_id = request.POST['brand']
    Ad = request.POST['ad']
    Alish = request.POST['alish']
    Satish = request.POST['satish']
    Miqdar = request.POST['miqdar']
    bsay = Mehsul.objects.filter(Brand_id=request.user.id,Ad=request.user.id).count()

    if bsay==0: 
        r=Brands.objects.get(id=Brand_id)
        add= Mehsul(Brand_id=r,Foto=uploaded_file_url,Ad=Ad,Alish=Alish,Satish=Satish,Miqdar=Miqdar,user_id=request.user.id)
        add.save()
        messages.success(request, 'Mehsul anbara uğurla əlavə edildi')
    else:
        messages.warning(request, 'Bu Mehsul artıq mövcuddur')

    return HttpResponseRedirect(reverse('mehsul'))
def deletemehsul(request,id):
    
    sifaris_yoxla = Sifaris.objects.filter(Mehsul_id_id=id).count()

    if sifaris_yoxla == 0:
        meh_id=Mehsul.objects.get(id=id)
        meh_id.delete()
        messages.success(request,'Ugurla silindi')
    else:
        messages.warning(request,'Bu mehsul hal-hazirda aktivdir') 
    return HttpResponseRedirect(reverse('mehsul'))
# def deleteconfmehsul(request,id):
#     mehsul=Mehsul.objects.filter(user_id=request.user.id).select_related().order_by('-id')
#     my_brands=Brands.objects.filter(user_id=request.user.id)
#     bsay = Mehsul.objects.filter(user_id=request.user.id).count()
#     deleteconfmehsul = Mehsul.objects.get(id=id)
#     template=loader.get_template('main/mehsul.html')
#     data = {'mehsul': mehsul,'my_brands':my_brands,"bsay":bsay,"deleteconfmehsul":deleteconfmehsul}
#     return HttpResponse(template.render(data,request))
    
    
def updatemehsul(request,id):
    info = Mehsul.objects.get(id=id)
    mehsul = Mehsul.objects.filter(user_id=request.user.id).order_by('-id')
    bsay = Mehsul.objects.filter(user_id=request.user.id).count()
    my_brands=Brands.objects.filter(user_id=request.user.id)

    template = loader.get_template('main/mehsul.html')
    data={'mehsul':mehsul,'bsay':bsay,'editmehsul':info,'my_brands':my_brands}

    return HttpResponse(template.render(data,request))
  
def updaterecordmehsul(request, id):
    if request.method=='POST' and 'foto' in request.FILES:
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)
    else:
        uploaded_file_url = request.POST['cari_mehsul']

    bid = request.POST['brand']
    Ad = request.POST['ad']
    Alish = request.POST['alish']
    Satish = request.POST['satish']
    Miqdar = request.POST['miqdar']
  
    bsay = Mehsul.objects.filter(user_id=request.user.id).exclude(id=id).count()

    if bsay==0:
        r = Brands.objects.get(user_id = bid)
        member = Mehsul.objects.get(id=id)
        member.Brand_id = r
        member.Ad = Ad
        member.Foto = uploaded_file_url
        member.Alish = Alish
        member.Satish = Satish
        member.Miqdar = Miqdar
        member.save()
        messages.success(request, 'Brend uğurla yenilendi')
    else:
        messages.warning(request, 'Bu brend artıq mövcuddur')
   
    return HttpResponseRedirect(reverse('mehsul'))
# Sifaris

def sifaris(request):
    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/sifaris.html',{'img':img})


def ajaxsifaris(request):
    section = 'sifaris'

    if 'sil_id' in request.GET:
        sifaris=Sifaris.objects.get(id=request.GET['sil_id'])
        sifaris.delete()
        messages.success(request,'Ugurla silindi')
        return HttpResponseRedirect(reverse('sifaris'))

    if 'sifarisinsert' in request.POST:

        Client_id = request.POST['ad_soyad']
        Mehsulid = request.POST['product']
        Miqdar = request.POST['miqdar']
        
        
        r=Clients.objects.get(id=Client_id)
        mehsultosifaris = Mehsul.objects.get(id=Mehsulid)
        daxilet = Sifaris(Client_id=r,Mehsul_id=mehsultosifaris,Miqdar=Miqdar,Tesdiq=0,user_id=request.user.id)
        daxilet.save()
        messages.success(request,'Ugurla Elave olundu')

    if 'edit_id' in request.GET:
        info = Sifaris.objects.get(id=request.GET['edit_id'])
        sifarish=Sifaris.objects.filter(user_id=request.user.id).select_related().order_by('-id')
        myclients=Clients.objects.filter(user_id=request.user.id)
        mehsul = Mehsul.objects.filter(user_id=request.user.id).select_related()
        bsay = Sifaris.objects.filter(user_id=request.user.id).count()
        data = {'sifarish': sifarish,'editsifaris':info,"myclients":myclients,"mehsul":mehsul,'bsay':bsay,'section':section}
        return render(request,'main/loader.html',data)
    
    if 'sifarisupdate' in request.POST:
        
        sif = Sifaris.objects.get(id=request.POST['id'])
        
        if sif.Miqdar >= sif.Mehsul_id.Miqdar:
            Client_id = request.POST['ad_soyad']
            Mehsulid =request.POST['product']
            Miqdar = request.POST['miqdar']
            r = Clients.objects.get(id = sif.Client_id_id)
            w = Mehsul.objects.get(id= sif.Mehsul_id_id)
            savesifaris = Sifaris.objects.get(id=request.POST['id'])
            savesifaris.Client_id=r
            savesifaris.Mehsul_id=w
            savesifaris.Miqdar = Miqdar
            savesifaris.save()
            messages.success(request,'Ugurla Yenilendi')
        else:
            messages.warning(request,'Bazada kifayet qeder mehsul yoxdur')
            
   
        

    
    sifarish=Sifaris.objects.filter(user_id=request.user.id).select_related().order_by('-id')
    myclients=Clients.objects.filter(user_id=request.user.id)
    mehsul = Mehsul.objects.filter(user_id=request.user.id).select_related()
    
    bsay = Sifaris.objects.filter(user_id=request.user.id).count()
    sayklient = Clients.objects.filter(user_id=request.user.id).count()
    saybrend = Brands.objects.filter(user_id=request.user.id).count()
    saymehsul = Mehsul.objects.filter(user_id=request.user.id).values_list('Miqdar').count()
    cesid = Mehsul.objects.filter(user_id=request.user.id).values_list('Ad').distinct().count()
    mehsulsayi = Mehsul.objects.filter(user_id=request.user.id).values_list('Miqdar', flat=True)
    mehsuldepo = sum(mehsulsayi)
    mehsulal = Mehsul.objects.filter(user_id=request.user.id).values_list("Alish",flat=True)
    alisdepo = sum(mehsulal)
    mehsulsat = Mehsul.objects.filter(user_id=request.user.id).values_list("Satish",flat=True)
    satisdepo = sum(mehsulsat)
    
    mehsulselect = Mehsul.objects.filter(user_id=request.user.id)
    qazancmehsul =0
    for x in mehsulselect:
        qazancmehsul = ((x.Satish - x.Alish) *  x.Miqdar) + qazancmehsul 
    # cari qazanc
    cariqaz = 0
    for y in sifarish:
        
        if y.Tesdiq == 1 :
            cariqaz = (int(y.Mehsul_id.Satish) * int(y.Miqdar)) - (int(y.Mehsul_id.Alish) * int(y.Miqdar)) + cariqaz
        

    
    template=loader.get_template('main/loader.html')
    data = {'sifarish': sifarish,"myclients":myclients,"mehsul":mehsul,"bsay":bsay,"sayklient":sayklient
    ,"saybrend":saybrend,"saymehsul":saymehsul,"cesid":cesid,"mehsuldepo":mehsuldepo,"alisdepo":alisdepo,
    "satisdepo":satisdepo,"qazanc":qazancmehsul,"cariqaz":cariqaz,'section':section}
    return HttpResponse(template.render(data,request))
"""   
def addsifaris(request):
    Client_id = request.POST['ad_soyad']
    Mehsulid = request.POST['product']
    Miqdar = request.POST['miqdar']
    
    
    r=Clients.objects.get(id=Client_id)
    mehsultosifaris = Mehsul.objects.get(id=Mehsulid)
    daxilet = Sifaris(Client_id=r,Mehsul_id=mehsultosifaris,Miqdar=Miqdar,Tesdiq=0,user_id=request.user.id)
    daxilet.save()
 
    return HttpResponseRedirect(reverse('sifaris'))
"""
 
def editsifaris(request,id):
    info = Sifaris.objects.get(id=id)
    sifarish=Sifaris.objects.filter(user_id=request.user.id).select_related().order_by('-id')
    myclients=Clients.objects.filter(user_id=request.user.id)
    mehsul = Mehsul.objects.filter(user_id=request.user.id).select_related()
    bsay = Sifaris.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/sifaris.html')
    data = {'sifarish': sifarish,'editsifaris':info,"myclients":myclients,"mehsul":mehsul,'bsay':bsay,}
    return HttpResponse(template.render(data,request))
    
def updatesifaris(request,id):
    Klid = request.POST['ad_soyad']
    Mehsulin =request.POST['product']
    Miqdar = request.POST['miqdar']
    r = Clients.objects.get(user_id = Klid)
    w = Mehsul.objects.get(user_id=Mehsulin)
    savesifaris = Sifaris.objects.get(id=id)
    savesifaris.Client_id=r
    savesifaris.Mehsul_id=w
    savesifaris.Miqdar = Miqdar
    savesifaris.save()

    return HttpResponseRedirect(reverse('sifaris'))

def deletesifaris(request,id):
    
    sifaris=Sifaris.objects.get(id=id)
    sifaris.delete()
    messages.success(request,'Ugurla silindi')
    return HttpResponseRedirect(reverse('sifaris'))



def tesdiq(request):
        pid = int(request.POST['pid'])
        sid = int(request.POST['sid'])
        smiq = int(request.POST['smiq'])
        pmiq = int(request.POST['pmiq'])

        sifaris=Sifaris.objects.get(id=sid)
        product = Mehsul.objects.get(id=pid)

        if smiq <= pmiq:
            netice = pmiq - smiq
            product.Miqdar=netice
            product.save()
            sifaris.Tesdiq=1
            sifaris.save()

            messages.success(request,'Ugurla tesdiqlendi')
        else:
            messages.warning(request,('Sifarisi tesdiq etmek ucun anbarda kifayet qeder mehsul yoxdur'))
        return HttpResponseRedirect(reverse('sifaris'))

def legv(request, id):

    if request.method =='GET':
        sifaris = Sifaris.objects.get(id=id)
        product = Mehsul.objects.get(id = sifaris.Mehsul_id_id)
        smiq = sifaris.Miqdar
        pmiq = product.Miqdar
        netice = int(pmiq) + int(smiq)

        product.Miqdar = netice
        product.save()

        sifaris.Tesdiq=0
        sifaris.save()

    messages.warning(request,'Ugurla legv edildi')
    
            
    return HttpResponseRedirect(reverse('sifaris'))
    
    
def shobe(request) :
    
    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/shobe.html',{'img':img})

def ajaxshobe(request):
    section = 'shobe'

    if 'sil_id' in request.GET:
        shobe=Shobe.objects.get(id=request.GET['sil_id'])
        yoxla= Vezife.objects.filter(shobe_id_id=request.GET['sil_id']).count()
        if yoxla == 0 :
            shobe.delete()
        else:
            messages.warning(request,'Bu shobeye aid Aktiv vezife var')
        return HttpResponseRedirect(reverse('shobe'))
    
    if 'shobe_insert' in request.POST:
        ad = request.POST['shobe']
        
        save = Shobe(ad=ad,user_id = request.user.id)
        save.save()
    
    
        
    shobe = Shobe.objects.filter(user_id=request.user.id).order_by('-id')
    say = Shobe.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/loader.html')
    data={'shobe':shobe,'bsay':say,'section':section,'vezife':vezife}
    return HttpResponse(template.render(data,request))

def vezife(request) :
    
    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/vezife.html',{'img':img})

def ajaxvezife(request):
    section = 'vezife'
    

    if 'sil_id' in request.GET:
        staff=Vezife.objects.get(id=request.GET['sil_id'])
        staff.delete()
        return HttpResponseRedirect(reverse('vezife'))
    
    if 'vezife_insert' in request.POST:
        ad = request.POST['vezife']
        shobe_id = request.POST['shobe_id']
        r = Shobe.objects.get(id = shobe_id)
        save = Vezife(ad=ad,user_id = request.user.id , shobe_id= r)
        save.save()
        
    vezife = Vezife.objects.filter(user_id=request.user.id).order_by('-id')
    say = Vezife.objects.filter(user_id=request.user.id).count()
    shobe = Shobe.objects.all()
    template=loader.get_template('main/loader.html')
    data={'vezife':vezife,'bsay':say,'section':section,'shobe':shobe}
    return HttpResponse(template.render(data,request))
    
    
    
# Ishciler


def staff(request):
    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/staff.html',{'img':img})

def ajaxstaff(request):
    section = 'staff'
    if request.POST.getlist('x[]'):    
        if request.method=='POST':
            for x in request.POST.getlist('x[]'):
                sil = Ishciler.objects.get(id=x)
                sil.delete()
        return HttpResponseRedirect(reverse('staff'))
    
    
    if 'sil_id' in request.GET:
        staff=Ishciler.objects.get(id=request.GET['sil_id'])
        staff.delete()
        return HttpResponseRedirect(reverse('staff'))
    
    
        

    if 'staffinsert' in request.POST:
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        telefon = request.POST['telefon']
        ev_tel=  request.POST['ev_tel']
        unvan = request.POST['unvan']
        email = request.POST['email']
        vezife = request.POST['vezife_id']
        
        r = Vezife.objects.get(id = vezife)
        
        daxilet = Ishciler(ad=ad,soyad=soyad, telefon=telefon,ev_tel=ev_tel,unvan=unvan,email=email,vezife_id=r,user_id=request.user.id)
            
        daxilet.save()

    if 'edit_id' in request.GET:
        staff = Ishciler.objects.filter(user_id=request.user.id).order_by('-id')
        say = Ishciler.objects.filter(user_id=request.user.id).count()
        editstaff = Ishciler.objects.get(id=request.GET['edit_id'])
        data={'staff':staff,'say':say,"editstaff":editstaff,'section':section}
        return render(request,'main/loader.html',data)

    if 'staffupdate' in request.POST:
        
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        telefon = request.POST['telefon']
        ev_tel=  request.POST['ev_tel']
        unvan = request.POST['unvan']
        email = request.POST['email']
        vezife = request.POST['vezife_id']
        savestaff = Ishciler.objects.get(id=request.POST['id'])
        r = Vezife.objects.get(id = savestaff.vezife_id_id)
        savestaff.vezife_id = r
        savestaff.ad=ad
        savestaff.soyad=soyad
        savestaff.telefon=telefon
        savestaff.ev_tel=ev_tel
        savestaff.unvan=unvan
        savestaff.email=email
        savestaff.save()
        
    vezife_id=Vezife.objects.filter(user_id=request.user.id)
    shobe = Shobe.objects.filter(user_id=request.user.id).order_by('-id')
    staff = Ishciler.objects.filter(user_id=request.user.id).order_by('-id')
    say = Ishciler.objects.filter(user_id=request.user.id).count()
    template=loader.get_template('main/loader.html')
    data={'staff':staff,'bsay':say,'section':section,'vezife_id':vezife_id,'shobe':shobe}
    return HttpResponse(template.render(data,request))

def addstaff(request):
    ad = request.POST['ad']
    soyad = request.POST['soyad']
    telefon = request.POST['telefon']
    ev_tel=  request.POST['ev_tel']
    unvan = request.POST['unvan']
    email = request.POST['email']
    vezife = request.POST['vezife']
    
    daxilet = Ishciler(ad=ad,soyad=soyad,telefon=telefon,ev_tel=ev_tel,unvan=unvan,email=email,vezife=vezife,user_id=request.user.id)
        
    daxilet.save()
    return HttpResponseRedirect(reverse('staff'))



def updatestaff(request,id):
    ad = request.POST['ad']
    soyad = request.POST['soyad']
    telefon = request.POST['telefon']
    ev_tel=  request.POST['ev_tel']
    unvan = request.POST['unvan']
    email = request.POST['email']
    vezife = request.POST['vezife']
    savestaff = Ishciler.objects.get(id=id)
    savestaff.ad=ad
    savestaff.soyad=soyad
    savestaff.telefon=telefon
    savestaff.ev_tel=ev_tel
    savestaff.unvan=unvan
    savestaff.email=email
    savestaff.vezife=vezife
    savestaff.save()
    return HttpResponseRedirect(reverse('staff'))

def deleteconfstaff(request,id):
    staff = Ishciler.objects.filter(user_id=request.user.id).order_by('-id')
    say = Ishciler.objects.filter(user_id=request.user.id).count()
    deletest = Ishciler.objects.get(id=id)
    template=loader.get_template('main/staff.html')
    data={'staff':staff,'say':say,"deletest":deletest}
    return HttpResponse(template.render(data,request))

def deletestaff(request,id):
    
    staff=Ishciler.objects.get(id=id)
    staff.delete()
    return HttpResponseRedirect(reverse('staff'))
# Senedler

def senedler(request,id):

    img = Profil.objects.filter(user_id_id = request.user.id)

    return render(request,'main/senedler.html',{'img':img,'id': id})

def ajaxsenedler(request ):
    

    section = 'senedler'
    if request.POST.getlist('x[]'):    
        if request.method=='POST':
            for x in request.POST.getlist('x[]'):
                sil = Senedler.objects.get(id=x)
                sil.delete()
        return HttpResponseRedirect(reverse('vezife'))

    if 'sil_id' in request.GET:

        deletesen = Senedler.objects.get(id = request.GET['sil_id'])
        image = str(settings.BASE_DIR) + str(deletesen.skan)
        os.remove(image)
        deletesen.delete()
        messages.success(request,'Ugurla Silindi')
        return HttpResponseRedirect(reverse('staff'))

    if 'senedinsert' in request.POST:

        if request.method=='POST' and request.FILES['foto']:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)
            isci_id = request.POST['isci_id']
            basliq = request.POST['basliqs']
            qeyd = request.POST['qeyds']
            r = Ishciler.objects.get(id = isci_id)
            
            daxilet = Senedler(ishci_id=r, basliq=basliq,skan=uploaded_file_url,qeyd=qeyd,user_id = request.user.id)
                
            daxilet.save()
    if 'edit_id' in request.GET:
        editsened = Senedler.objects.get(id = request.GET['edit_id'])
        staff = Ishciler.objects.all()
        senedler = Senedler.objects.all().order_by('-id')
        say = Senedler.objects.all().count()
        sened_id = Senedler.objects.filter(user_id = request.user.id).select_related()
        data={'senedler':senedler,'bsay':say,"staff":staff,"sened_id":sened_id,'section':section,'editsened':editsened}
        return render(request,'main/loader.html',data)
    if 'update_sened' in request.POST:
        if request.method=='POST' and 'foto' in request.FILES:
            foto=request.FILES['foto']
            fs = FileSystemStorage()
            filename=fs.save(foto.name,foto)
            uploaded_file_url=fs.url(filename)
            isci_id = request.POST['isci_id']
            basliq = request.POST['basliqs']
            qeyd = request.POST['qeyds']

            savesened = Senedler.objects.get(id=request.POST['id'])
            r =  Ishciler.objects.get(id=savesened.ishci_id_id)
            
            savesened.ishci_id = r
            savesened.basliq = basliq
            savesened.skan = uploaded_file_url
            savesened.qeyd = qeyd
            savesened.save()

    staff = Ishciler.objects.all()
    say = Senedler.objects.all().count()
    sened_id = Senedler.objects.filter(Q(user_id = request.user.id) ).select_related()
    senedler = Senedler.objects.all()
    template=loader.get_template('main/loader.html')
    data={'bsay':say,"staff":staff,"sened_id":sened_id,'section':section,'senedler':senedler}
    return HttpResponse(template.render(data,request))

def addsenedler(request):
    if request.method=='POST' and 'foto' in request.FILES:
        foto=request.FILES['foto']
        fs = FileSystemStorage()
        filename=fs.save(foto.name,foto)
        uploaded_file_url=fs.url(filename)
    isci_id = request.POST['isci_id']
    basliq = request.POST['basliqs']
    qeyd = request.POST['qeyds']
    r = Ishciler.objects.get(id = isci_id)
    
    daxilet = Senedler(ishci_id=r, basliq=basliq,skan=uploaded_file_url,qeyd=qeyd)
        
    daxilet.save()
    return HttpResponseRedirect(reverse('senedler'))


def user_admin(request):
    return render (request,'main/user_admin.html')









            