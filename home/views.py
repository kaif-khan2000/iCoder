from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Html pages
def home(request):
    return render(request,'home/home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        content = request.POST.get("content")
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please Enter the form Correctly")
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Sucessfull!...")
    return render(request,"home/contact.html")

def about(request):
    return render(request,"home/about.html")

def search(request):
    query = request.GET.get("query")
    if len(query)>80:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"Search results not found.")
    
    return render(request,"home/search.html",{'allPosts':allPosts,'query':query})

#Authentication apis
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        #validate form 
        if len(username) > 10:
            messages.error(request,"your username nust be under 10")
        elif pass1!=pass2:
            messages.error(request,"Passwords do not match. ")
        
        elif not username.isalnum():
            messages.error(request,"Only numbers and alphabets should be used.(No spaces)")
        
        else:
            #create the user
            myuser = User.objects.create_user(username,email,pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,"your account successfully created")
        
        return redirect('home')

    else:
        return HttpResponse('<h2>404-Page not found</h2>')

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST["loginusername"]
        pass1 = request.POST["loginpass"]

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request,user)
            messages.success(request,"sucessfully logged in")
        else:
            messages.error(request,"Invalid Credentials")
    else: return HttpResponse('<h2>404- page not found</h2>')
    return redirect('home')

def handleLogout(request):
    logout(request)
    messages.success(request,"loged out successfull")
    return redirect('home')


