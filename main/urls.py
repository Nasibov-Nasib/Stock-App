from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
import random

urlpatterns=[
    # Forgot password 
    path("mail_send/", views.mail_send, name="mail_send"),
    path("accounts/login/change_pass_page/", views.change_pass_page, name="change_pass_page"),
    path("accounts/login/change_pass_page/change_pass/<int:id>", views.change_pass, name="change_pass"),
    

    

    path('accounts/login/reset_password/',auth_views.PasswordResetView.as_view() , name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view() , name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view() , name='password_reset_complete'),

    # Search
    # path('axtar/',views.axtar,name='axtar'),
    path('clients/axtarclient/',views.axtarclient,name='axtarclient'),
    # path("block_user/", views.block_user, name="block_user"),
    # Login
    path("register/", views.register, name="register"),
    path("accounts/login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("deleteuser/<int:id>", views.deleteuser, name="deleteuser"),
    path("deluserconfirm/<int:id>", views.deluserconfirm, name="deluserconfirm"),

    # Profil
    path('profile/',views.profile,name='profile'),
    path('profile/updateprofile/<int:id>',views.updateprofile,name='updateprofile'),


    # Brends
    path('',views.index,name='index'),
    path('loader/',views.ajaxloader,name='loader'),
    path('addbrand/',views.addbrand,name='addbrand'),
    #path('deleteconfirm/<int:id>',views.deleteconfirm,name='deleteconfirm'),
    # path('deleteconfirm/delete/<int:id>',views.delete,name='delete'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('edit/update/<int:id>', views.update, name='update'),
    path('delete_all/',views.delete_all,name='delete_all'),


    # Clients
    path('clients/',views.clients,name='clients'),
    path('clients/loader/',views.ajaxclients,name='loader'),
    path('clients/addclient/',views.addclient,name='addclient'),
    # path('clients/deleteconfirmclient/<int:id>',views.deleteconfirmclient,name='deleteconfirmclient'),
    path('clients/deleteconfirmclient/deleteclient/<int:id>',views.deleteclient,name='deleteclient'),
    path('clients/updateclients/<int:id>',views.updateclients,name='updateclients'),
    path('clients/updateclients/updaterecordclients/<int:id>', views.updaterecordclients, name='updaterecordclients'),
    
    # Xercler
    path('xercler/',views.xercler,name='xercler'),
    path('xercler/loader/',views.ajaxxercler,name='loader'),
    path('xercler/addxercler/',views.addxercler,name='addxercler'),
    path('xercler/deletexercler/<int:id>',views.deletexercler,name='deletexercler'),
    path('xercler/updatexercler/<int:id>',views.updatexercler,name='updatexercler'),
    path('xercler/updatexercler/updaterecordxercler/<int:id>', views.updaterecordxercler, name='updaterecordxercler'),
    
    # Mehsul
    path('mehsul/',views.mehsul,name='mehsul'),
    path('mehsul/loader/',views.ajaxmehsul,name='loader'),
    path('mehsul/addmehsul/',views.addmehsul,name='addmehsul'),
    # path('mehsul/deleteconfmehsul/<int:id>',views.deleteconfmehsul,name='deleteconfmehsul'),
    path('mehsul/deleteconfmehsul/deletemehsul/<int:id>',views.deletemehsul,name='deletemehsul'),
    path('mehsul/updatemehsul/<int:id>',views.updatemehsul,name='updatemehsul'),
    path('mehsul/updatemehsul/updaterecordmehsul/<int:id>', views.updaterecordmehsul, name='updaterecordmehsul'),

    # Sifaris
    path('sifaris/',views.sifaris,name='sifaris'),
    path('sifaris/loader/',views.ajaxsifaris,name='loader'),
    # path('sifaris/addsifaris/',views.addsifaris,name='addsifaris'),
    # path('sifaris/deletesifarisconf/<int:id>',views.deletesifarisconf,name='deletesifarisconf'),
    path('sifaris/deletesifarisconf/deletesifaris/<int:id>',views.deletesifaris,name='deletesifaris'),
    path('sifaris/editsifaris/<int:id>',views.editsifaris,name='editsifaris'),
    path('sifaris/editsifaris/updatesifaris/<int:id>',views.updatesifaris,name='updatesifaris'),
    path('sifaris/tesdiq/',views.tesdiq,name='tesdiq'),
    path('sifaris/legv/<int:id>',views.legv,name='legv'),

    # Isciler
    path('staff/',views.staff,name='staff'),
    path('staff/loader/',views.ajaxstaff,name='loader'),
    path('staff/addstaff/',views.addstaff,name='addstaff'),
    # path('staff/editstaff/<int:id>',views.editstaff,name='editstaff'),
    path('staff/editstaff/updatestaff/<int:id>',views.updatestaff,name='updatestaff'),
    path('staff/deleteconfstaff/<int:id>',views.deleteconfstaff,name='deleteconfstaff'),
    path('staff/deleteconfstaff/deletestaff/<int:id>',views.deletestaff,name='deletestaff'),

    # Senedler
    path('staff/senedler/<int:id>',views.senedler,name='senedler'),
    path('staff/senedler/loader/',views.ajaxsenedler,name='loader'),
    path('staff/senedler/addsenedler/',views.addsenedler,name='addsenedler'),
    
    # Shobe
    path('shobe/',views.shobe,name='shobe'),
    path('shobe/loader/',views.ajaxshobe,name='loader'),
    
    # Vezife
    path('vezife/',views.vezife,name='vezife'),
    path('vezife/loader/',views.ajaxvezife,name='loader'),
    # ADmin
    path('users/',views.users,name='users'),
    path('users/loader/',views.ajaxusers,name='loader'),
    path('users/block_user/<int:id>',views.block_user,name='block_user'),
    path('users/active_user/<int:id>',views.active_user,name='active_user'),
    
    #To do app
    
    path('deleteapp/<int:id>',views.deleteapp,name='deleteapp'),
    path('sil/<int:id>',views.sil,name='sil'),
    path('editapp/<int:id>',views.editapp,name='editapp'),
    path('updateapp/<int:id>',views.updateapp,name='updateapp'),
    path('filter_id/<int:id>',views.secim,name='secim'),
    path('todoapp/',views.todoapp,name='todoapp'),
    path('excel',views.excel,name='excel'),


    


] 
