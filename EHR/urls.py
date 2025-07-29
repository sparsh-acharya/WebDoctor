"""
URL configuration for EHR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from user import views as user_views
from doctor import views as doc_views
from patients import views as pat_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls, name='ADMIN'),

    #Auth URL
    path('', user_views.regpat, name='reg'),
    path('login/', user_views.UserLogin, name='login'),
    path('logout/', user_views.UserLogout, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="auth/reset_password.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="auth/reset_password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="auth/change_password.html"),name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="auth/reset_password_complete.html"),name="password_reset_complete"),


    #Doc URL
    path('doctor/home',doc_views.DocDash, name='DOC'),
    path('doctor/My-Patients',doc_views.DocPats, name='DOC_PATS'),
    path('doctor/patient/<int:patient_id>/', doc_views.patient_detail, name='DOC_PAT_DETAIL'),
    path('doctor/patient/<int:patient_id>/edit-vitals/', doc_views.edit_vitals, name='EDIT_VITALS'),
    path('doctor/medication/edit/<int:med_id>/', doc_views.edit_medication, name='EDIT_MED'),
    path('doctor/medication/add/<int:pat_id>/', doc_views.add_medication, name='ADD_MED'),
    path('doctor/medication/delete/<int:med_id>/', doc_views.delete_medication, name='DELETE_MED'),
    path('doctor/patient/<int:patient_id>/reports/add', doc_views.add_patient_report, name='DOC_ADD_PATIENT_REPORT'),
    path('doctor/patient/<int:patient_id>/reports/<int:report_id>/edit', doc_views.edit_patient_report, name='DOC_EDIT_PATIENT_REPORT'),
    path('doctor/patient/<int:patient_id>/reports/<int:report_id>/get-edit-form', doc_views.get_report_edit_form, name='DOC_GET_REPORT_EDIT_FORM'),
    path('doctor/patient/<int:patient_id>/reports/<int:report_id>/delete', doc_views.delete_patient_report, name='DOC_DELETE_PATIENT_REPORT'),
    path('doctor/patient/<int:patient_id>/reports/<int:report_id>/view', doc_views.view_patient_report, name='DOC_VIEW_PATIENT_REPORT'),
    path('doctor/patient/<int:patient_id>/reports/<int:report_id>/download', doc_views.downloadReport, name='DOC_DOWNLOAD_REPORT'),
    path('doctor/requests',doc_views.DocReq, name='DOC_REQ'),
    path('doctor/request/<int:request_id>/approve', doc_views.approve_request, name='DOC_APPROVE'),
    path('doctor/request/<int:request_id>/reject', doc_views.reject_request, name='DOC_REJECT'),
    path('doctor/appointments/', doc_views.doctor_appointments, name='DOC_APOI'),
    path('doctor/appointments/create/', doc_views.create_appointment, name='DOC_C_APOI'),
    path('doctor/appointments/<int:ap_id>/edit/', doc_views.edit_appointment, name='DOC_E_APOI'),
    path('doctor/appointments/<int:ap_id>/get-data/', doc_views.get_appointment_data, name='DOC_GET_APOI_DATA'),
    path('doctor/appointments/<int:ap_id>/cancel/', doc_views.cancel_appointment, name='DOC_CAN_APOI'),
    path('doctor/patient/<int:patient_id>/medications/<int:med_id>/get-edit-form', doc_views.get_med_edit_form, name='DOC_GET_MED_EDIT_FORM'),
    path('doctor/patient/<int:patient_id>/get-edit-vitals-form', doc_views.get_edit_vitals_form, name='DOC_GET_EDIT_VITALS_FORM'),
   


    #Pat URL
    path('patient/home',pat_views.PatDash, name='PAT'),
    path('patient/explore', pat_views.ExploreDoctors, name='PAT_EXPLORE'),
    path('patient/medications', pat_views.PatMedication, name='PAT_MEDS'),
    path('patient/reports', pat_views.PatReports, name='PAT_REPORTS'),
    path('patient/reports/add', pat_views.AddReport, name='PAT_ADD_REPORT'),
    path('patient/reports/<int:report_id>/edit', pat_views.EditReport, name='PAT_EDIT_REPORT'),
    path('patient/reports/<int:report_id>/view', pat_views.ViewReport, name='PAT_VIEW_REPORT'),
    path('patient/reports/<int:report_id>/delete', pat_views.DeleteReport, name='PAT_DELETE_REPORT'),
    path('patient/reports/<int:report_id>/download', pat_views.DownloadReport, name='PAT_DOWNLOAD_REPORT'),
    path('send-connection-request/', pat_views.SendConnectionRequest, name='SEND_CONNECTION_REQUEST'),


    path('patient/appointments/', pat_views.patient_appointments, name='PAT_APOI'),

]

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
