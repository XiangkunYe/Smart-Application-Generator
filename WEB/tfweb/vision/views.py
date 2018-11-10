
import datetime

from django.shortcuts import render, render_to_response
import os
# Create your views here.
from django.http import HttpResponse
from django.db import connection
from tfweb.settings import LOGIN_REDIRECT_URL
from vision.form import UploadFileForm

from .models import User, Project, Task, Model
from django.contrib.auth.decorators import login_required


def index(request):
    """
    View function for home page of site.
    """
    # num_user = User.objects.all().count()
    # num_project = Project.objects.all().count()
    # num_model = Model.objects.all().count()
    # num_task = Task.objects.count()
    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable
    return render(request,'index.html',)



from django.core.files.storage import FileSystemStorage
import os

def upload_file(request):
    folder = os.path.join('media/',str(request.user.id),str(Project.id))
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=folder)
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html')


def TutorialView(request):
    return render(request,'tutorial.html')

def AboutView(request):
    return render(request, 'about.html')

def ContactView(request):
    return render(request, 'contact.html')

@login_required(login_url='/accounts/login/')
def MainView(request):

    return render(request, 'mainpage.html')


    uid = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT svag_db.vision_project.id, svag_db.vision_project.name, svag_db.vision_task.state "
                       "FROM svag_db.vision_project "
                       "left join svag_db.vision_task on svag_db.vision_project.id = svag_db.vision_task.project_id "
                       "where svag_db.vision_project.user_id = %s", [uid])
        rows = cursor.fetchall()
    projects = []
    for row in rows:
        if row[2] is None:
            projects.append({'name': row[1], 'state': 'waiting response'})
        else:
            projects.append({'name': row[1], 'state': row[2]})
    return render(request, 'mainpage.html', {'username': request.user.username,
                                             'projects': projects})


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/accounts/login/')

    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})