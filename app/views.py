from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import JobCategory, Job, JobApplication
from django.contrib.auth.decorators import login_required
User = get_user_model()
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def AdminLogin(request):
    return render(request, 'admin/login.html')


@login_required(login_url='candidate-login')
def AdminDashboard(request):
    total_user=User.objects.filter(is_superuser=False).only('id').count()
    total_jobs=Job.objects.only('id').count()
    total_applications=JobApplication.objects.only('id').count()

    recent_jobs = Job.objects.select_related('category').prefetch_related('applications').order_by('-created_at')[:3]
   

    context = {
        'user_count': total_user,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'recent_jobs': recent_jobs,
    }

    return render(request, 'admin/dashboard.html', context)






def Admin_create_job_category(request):
    
    if request.method == "POST" and "create_category" in request.POST:
        name = request.POST.get("name").strip()
        if not name:
            messages.error(request, "Category name cannot be empty.")
            return redirect("admin-job_category_add")

        if JobCategory.objects.filter(name__iexact=name).exists():
            messages.error(request, "This category already exists.")
            return redirect("admin-job_category_add")

        JobCategory.objects.create(name=name)
        messages.success(request, f"Category '{name}' created successfully.")
        return redirect("admin-job_category_add")



    # Handle delete category
    if request.method == "POST" and "delete_category" in request.POST:
        category_id = request.POST.get("category_id")
        category = get_object_or_404(JobCategory, id=category_id)
        category.delete()
        messages.success(request, f"Category deleted successfully.")
        return redirect("admin-job_category_add")

    # List all categories
    categories = JobCategory.objects.all()
    return render(request, "job/create_category.html", {"categories": categories})



@login_required(login_url='candidate-login')
def AdminJoblist(request):
    jobs = Job.objects.select_related('category').prefetch_related('applications').order_by('-created_at')
    return render(request, 'admin/joblisting.html', {'jobs': jobs})



@login_required(login_url='candidate-login')
def AdminJobpost(request):

    categories = JobCategory.objects.only("name")

    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("company", "").strip()
        location = request.POST.get("location")
        job_type = request.POST.get("job_type")
        category_id = request.POST.get("category")
        vacancies = request.POST.get("positions")
        experience = request.POST.get("experience")
        description = request.POST.get("full_description")
        requirements = request.POST.get("requirements")
        skills_raw = request.POST.get("skills")

        # Basic validation
        if not all([title, location, job_type, category_id, vacancies, description, requirements, skills_raw]):
            messages.error(request, "All mandatory fields are required.")
            return redirect("admin-jobpost")

        category = get_object_or_404(JobCategory, id=category_id)

        # Skills parsing (max 5)
        skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
        while len(skills) < 5:
            skills.append(None)

        Job.objects.create(
            title=title,
            company=company or "Confidential",
            location=location,
            job_type=job_type,
            skill_1=skills[0],
            skill_2=skills[1],
            skill_3=skills[2],
            skill_4=skills[3],
            skill_5=skills[4],
            experience=experience,
            vacancies=vacancies,
            required_qualification=requirements,
            description=description,
            category=category,
            posted_by=request.user,
        )

        messages.success(request, "Job posted successfully.")
        return redirect("admin-joblist")

    return render(request, "admin/jobpost.html", {
        "categories": categories
    })





@login_required(login_url='candidate-login')
def AdminJobEdit(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect("candidate-login")

    job_id = request.GET.get("id")
    job = get_object_or_404(Job, id=job_id)
    categories = JobCategory.objects.all()

    # Create comma-separated skills string for the template
    skills_list = [job.skill_1, job.skill_2, job.skill_3, job.skill_4, job.skill_5]
    skills_string = ", ".join([skill for skill in skills_list if skill])

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.company = request.POST.get("company", "Confidential")
        job.location = request.POST.get("location")
        job.job_type = request.POST.get("job_type")
        job.vacancies = request.POST.get("positions")
        job.experience = request.POST.get("experience")
        job.description = request.POST.get("full_description")
        job.required_qualification = request.POST.get("requirements")

        category_id = request.POST.get("category")
        job.category = get_object_or_404(JobCategory, id=category_id)

        skills = [s.strip() for s in request.POST.get("skills", "").split(",") if s.strip()]
        while len(skills) < 5:
            skills.append(None)

        job.skill_1, job.skill_2, job.skill_3, job.skill_4, job.skill_5 = skills[:5]

        job.save()
        messages.success(request, "Job updated successfully.")
        return redirect("admin-joblist")

    return render(request, "admin/jobedit.html", {
        "job": job,
        "categories": categories,
        "skills_string": skills_string
    })



@login_required(login_url='candidate-login')
def AdminJobDetails(request):
  
    job_id = request.GET.get("id")
    job = get_object_or_404(
        Job.objects.select_related("category", "posted_by")
                   .prefetch_related("applications__candidate"),
        id=job_id
    )

    # Create skills list for template
    skills_list = [job.skill_1, job.skill_2, job.skill_3, job.skill_4, job.skill_5]
    skills_list = [skill for skill in skills_list if skill]  

    return render(request, "admin/jobdetails.html", {
        "job": job,
        "skills_list": skills_list
    })



@login_required(login_url='candidate-login')
def AdminJobDelete(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect("candidate-login")

    job_id = request.GET.get("id")
    job = get_object_or_404(Job, id=job_id)

    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect("admin-joblist")





@login_required(login_url='candidate-login')
def AdminAllApplications(request):
    applications = JobApplication.objects.select_related("job", "candidate", "job__category").order_by("-applied_at")

    category_filter = request.GET.get("category")
    status_filter = request.GET.get("status")
    search_query = request.GET.get("search")

    if category_filter and category_filter != "All":
        applications = applications.filter(job__category_id=category_filter)

    if status_filter and status_filter != "All":
        applications = applications.filter(status=status_filter.lower())

    if search_query:
        applications = applications.filter(
            Q(candidate__email__icontains=search_query) |
            Q(candidate__designation__icontains=search_query) |
            Q(candidate__education__icontains=search_query)
        )

    categories = JobCategory.objects.all()

    context = {
        "applications": applications,
        "categories": categories,
        "status_choices": JobApplication.status_choices,
        "selected_category": category_filter or "All",
        "selected_status": status_filter or "All",
        "search_query": search_query or "",
    }

    return render(request, "admin/applications.html", context)






@login_required(login_url='candidate-login')
def admin_job_application_detail(request, application_id):


    application = get_object_or_404(JobApplication.objects.select_related('candidate', 'job'), id=application_id)

    if request.method == "POST":
        status = request.POST.get("status")
        notes = request.POST.get("notes", "")
        if status in dict(JobApplication.status_choices).keys():
            application.status = status
            application.notes = notes
            application.save()
            messages.success(request, f"Application status updated to {status.capitalize()}")
            return redirect('admin-applications-details', application_id=application.id)
        else:
            messages.error(request, "Invalid status selected.")

    context = {
        "application": application,
        "status_choices": JobApplication.status_choices,
    }
    return render(request, "admin/jobapplication_detail.html", context)




def AdminDeleteApplication(request, application_id):
    application=get_object_or_404(JobApplication, id=application_id)
    application.delete()
    messages.success(request, "Application deleted successfully.")
    return redirect("admin-applications")

# ---------------------------------------------------------------------------





def CandidateRegister(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("candidate-register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("candidate-register")

        user = User.objects.create_user(
            email=email,
            password=password1,
            designation=request.POST.get("designation"),
            education=request.POST.get("education"),
            phone=request.POST.get("phone"),
            location=request.POST.get("location"),
            resume=request.FILES.get("resume"),
        )

        user = authenticate(request, email=email, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("candidate-joblist")
        else:
            messages.error(request, "Registration succeeded but login failed. Please login manually.")
            return redirect("candidate-login")
    
    return render(request, 'candidate/register.html')


def CandidateLogin(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            if user.is_superuser or user.is_staff:
                return redirect("admin-dashboard")
            else:
                return redirect("candidate-joblist")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("candidate-login")
    return render(request, 'candidate/login.html')




def CandidateForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email:
            messages.error(request, "Email is required")
            return redirect("candidate-forgotpassword")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email")
            return redirect("candidate-forgotpassword")

        if not password1 or not password2:
            messages.error(request, "Please enter both password fields")
            return redirect("candidate-forgotpassword")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("candidate-forgotpassword")

        user.set_password(password1)
        user.save()

        messages.success(request, "Password reset successful. You can now login.")
        return redirect("candidate-joblist")

    return render(request, "candidate/forgotpassword.html")


def candidate_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("candidate-login")




def Candidateprofile(request):
    user = request.user

    context = {
        "user_obj": user,
    }
    return render(request, 'candidate/profile.html',context)



def candidate_editprofile(request):
    user = request.user

    if request.method == "POST":
        user.designation = request.POST.get("designation", "").strip()
        user.education = request.POST.get("education", "").strip()
        user.phone = request.POST.get("phone", "").strip()
        user.location = request.POST.get("location", "").strip()

        if request.FILES.get("resume"):
            user.resume = request.FILES["resume"]

        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("candidate-profile")

    return render(request, "candidate/edit_profile.html", {"user": user})






@login_required(login_url='candidate-login')
def CandidateJoblist(request):
    user = request.user

    jobs = Job.objects.select_related('category', 'posted_by') \
        .prefetch_related('applications') \
        .order_by('-created_at')

    search = request.GET.get('search')
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(skill_1__icontains=search) |
            Q(skill_2__icontains=search) |
            Q(skill_3__icontains=search) |
            Q(skill_4__icontains=search) |
            Q(skill_5__icontains=search)
        )

    category = request.GET.get('category')
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')

    if category:
        jobs = jobs.filter(category_id=category)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if location:
        jobs = jobs.filter(location__icontains=location)

    paginator = Paginator(jobs, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ---------------- APPLIED JOBS ----------------
    applied_job_ids = JobApplication.objects.filter(
        candidate=user
    ).values_list('job_id', flat=True)

    categories = JobCategory.objects.all()

    context = {
        "jobs": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "applied_job_ids": applied_job_ids,
        "total_jobs": paginator.count,
        "search": search,
        "selected_category": category,
        "selected_job_type": job_type,
        "location": location,
    }

    return render(request, 'candidate/joblisting.html', context)




@login_required(login_url='candidate-login')
def CandidateJobDetail(request, job_id):
    job = get_object_or_404(
        Job.objects.select_related('category', 'posted_by'),
        id=job_id
    )

    skills = [
        job.skill_1,
        job.skill_2,
        job.skill_3,
        job.skill_4,
        job.skill_5,
    ]
    skills = [s for s in skills if s]

    has_applied = JobApplication.objects.filter(
        candidate=request.user,
        job=job
    ).exists()

    context = {
        "job": job,
        "skills": skills,
        "has_applied": has_applied,
    }

    return render(request, 'candidate/jobdetail.html', context)




@login_required(login_url='candidate-login')
def CandidateJobApply(request, job_id):
    user = request.user
    job = get_object_or_404(Job, id=job_id)

    if JobApplication.objects.filter(candidate=user, job=job).exists():
        messages.warning(
            request,
            f"You have already applied for the job: {job.title}"
        )
        return redirect('candidate-jobdetail', job_id=job.id)

    JobApplication.objects.create(
        candidate=user,
        job=job,
        status='applied'
    )

    messages.success(
        request,
        f"Successfully applied for the job: {job.title}"
    )

    return redirect('candidate-joblist')




@login_required(login_url='candidate-login')
def CandidateJobAppliedList(request):
    applications = (
        JobApplication.objects
        .select_related('job', 'job__category')
        .filter(candidate=request.user)
        .order_by('-applied_at')
    )

    context = {
        "applications": applications,
        "total_applications": applications.count(),
        "reviewed_count": applications.filter(status='reviewed').count(),
        "shortlisted_count": applications.filter(status='shortlisted').count(),
        "rejected_count": applications.filter(status='rejected').count(),
        "hired_count": applications.filter(status='hired').count(),
    }

    return render(request, 'candidate/jobappliedlist.html', context)





def CandidateContact(request):
    return render(request, 'candidate/contact.html')