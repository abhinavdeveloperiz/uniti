from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard/',views.AdminDashboard, name='admin-dashboard'),
    path('admin/joblist/',views.AdminJoblist, name='admin-joblist'),
    path('admin/jobpost/',views.AdminJobpost, name='admin-jobpost'),
    path('admin/jobedit/',views.AdminJobEdit, name='admin-jobedit'),
    path('admin/jobdetails/',views.AdminJobDetails, name='admin-jobdetails'),
    path('admin/jobdelete/',views.AdminJobDelete, name='admin-jobdelete'),
    path('admin/applications/',views.AdminAllApplcations,name='admin-applications'),


    # ---------------------------------------------------------------------------- 
    path('candidate/',views.Candidateprofile, name='candidate-profile'),
    path('candidate/register/',views.CandidateRegister,name='candidate-register'),
    path('',views.CandidateJoblist, name='candidate-joblist'),
    path('candidate/jobdetail/',views.CandidateJobDetail, name='candidate-jobdetail'),
    path('candidate/jobapply/',views.CandidateJobApply, name='candidate-jobapply'),
    path('candidate/jobappliedlist/',views.CandidateJobAppliedList, name='candidate-jobappliedlist'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
