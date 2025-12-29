from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard/',views.AdminDashboard, name='admin-dashboard'),
    path('admin/joblist/',views.AdminJoblist, name='admin-joblist'),
    path('admin/job_category-add/',views.Admin_create_job_category, name='admin-job_category_add'),
    path('admin/jobpost/',views.AdminJobpost, name='admin-jobpost'),
    path('admin/jobedit/',views.AdminJobEdit, name='admin-jobedit'),
    path('admin/jobdetails/',views.AdminJobDetails, name='admin-jobdetails'),
    path('admin/jobdelete/',views.AdminJobDelete, name='admin-jobdelete'),
    path('admin/applications/',views.AdminAllApplications,name='admin-applications'),
    path('admin/applications/<int:application_id>/',views.admin_job_application_detail,name='admin-applications-details'),
    path('admin/applications/<int:application_id>/delete/',views.AdminDeleteApplication,name='admin-application-delete'),



    # ---------------------------------------------------------------------------- 
    path('candidate/',views.Candidateprofile, name='candidate-profile'),
    path("candidate/profile/edit/", views.candidate_editprofile, name="candidate-editprofile"),
    path('candidate/register/',views.CandidateRegister,name='candidate-register'),
    path('candidate/login/',views.CandidateLogin, name='candidate-login'),
    path('candidate/forgotpassword/',views.CandidateForgotPassword, name='candidate-forgotpassword'),
    path('candidate/logout/',views.candidate_logout, name='candidate-logout'),

    path('',views.CandidateJoblist, name='candidate-joblist'),
    path('candidate/jobdetail/<int:job_id>/',views.CandidateJobDetail, name='candidate-jobdetail'),
    path('candidate/jobapply/<int:job_id>/',views.CandidateJobApply, name='candidate-jobapply'),
    path('candidate/jobappliedlist/',views.CandidateJobAppliedList, name='candidate-jobappliedlist'),

    path('candidate/contact/',views.CandidateContact, name='candidate-contact'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
