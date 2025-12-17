from django.shortcuts import render

# Create your views here.

def AdminLogin(request):
    return render(request, 'admin/login.html')

def AdminDashboard(request):
    return render(request, 'admin/dashboard.html')

def AdminJoblist(request):
    return render(request, 'admin/joblisting.html')

def AdminJobpost(request):
    return render(request, 'admin/jobpost.html')

def AdminJobEdit(request):
    return render(request, 'admin/jobedit.html')

def AdminJobDetails(request):
    return render(request, 'admin/jobdetails.html')

def AdminJobDelete(request):
    return render(request, 'admin/jobdelete.html')


def AdminAllApplcations(request):
    return render(request,'admin/applications.html')


# ---------------------------------------------------------------------------


def CandidateRegister(request):
    return render(request, 'candidate/register.html')

def CandidateLogin(request):
    return render(request, 'candidate/login.html')

def CandidateForgotPassword(request):
    return render(request, 'candidate/forgotpassword.html')

def Candidateprofile(request):
    return render(request, 'candidate/profile.html')

def CandidateJoblist(request):
    return render(request, 'candidate/joblisting.html')

def CandidateJobDetail(request):
    return render(request, 'candidate/jobdetail.html')

def CandidateJobApply(request):
    return render(request, 'candidate/jobapply.html')

def CandidateJobAppliedList(request):
    return render(request, 'candidate/jobappliedlist.html')