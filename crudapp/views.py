from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm,LoginForm,CreateRecordForm,UpdateRecordForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record


# home
def home(request):
    return render(request, 'crudapp/index.html')


# register a user
def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    context = {'form':form}
    return render(request, 'crudapp/register.html', context=context)


# login
def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request,data=request.POST)

        if form.is_valid():

            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request, username=username, password=password) #checking the database username to the entered name
            if user is not None:

                auth.login(request, user)
                messages.success(request, "You have logged in")

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'crudapp/login.html', context=context)

# - Dashboard

@login_required(login_url='login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'crudapp/dashboard.html',context=context)


# - Create a record 

@login_required(login_url='login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")

            return redirect("dashboard")

    context = {'form': form}

    return render(request, 'crudapp/create-record.html', context=context)


# - Update a record 

@login_required(login_url='login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'crudapp/update-record.html', context=context)



# - Read / View a singular record

@login_required(login_url='login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'crudapp/view-record.html', context=context)


@login_required(login_url='login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")

# - User logout

def user_logout(request):

    auth.logout(request)

    messages.success(request, "Logout success!")

    return redirect("login")

