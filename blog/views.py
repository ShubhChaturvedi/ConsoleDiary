
from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Post ,BlogComment
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from blog.templatetags import extras
from django.core.files.storage import FileSystemStorage

def index(request):
    posts = Post.objects.all()
    lst = []
    blog={}
    for post in posts:
        comment = BlogComment.objects.filter(post = post)
        lst.append(len(comment))
        blog.update({post.sno : len(comment)})
    lst.sort(reverse=True)
    def get_key(val):
        for key, value in blog.items():
            if val == value:
                return key
    
   
    allpost1 = Post.objects.filter(sno = get_key(lst[0]))
    allpost2 = Post.objects.filter(sno = get_key(lst[1]))
    allpost3 = Post.objects.filter(sno = get_key(lst[2]))
    
    context = {'allblogs': [allpost1 , allpost2 , allpost3]}
    
    return render(request , 'blog/index.html' , context)

def contact(request):
    return render(request , 'blog/contact.html')

def about(request):
    return HttpResponse('hello aboutus')

def search(request):
    query = request.GET.get('query')
    allposts = Post.objects.filter(title__icontains=query)
    context = {'message':'to your search results' , 'allposts' : allposts}
    return render(request , 'blog/search.html' , context)

def blogs(request):
    allposts = Post.objects.all()
    context = {'message':'','allposts' : allposts}
    return render(request , 'blog/blogs.html' , context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # error check
        if pass1 !=pass2 :
            params = {'message' : 'Password not matched!!!...'}
            return render(request , 'blog/register.html' , params)
        if len(username) > 10 :
            params = {'message' : 'Username is out of bound!!!...'}
            return render(request , 'blog/register.html' , params)
        if not username.isalnum() :
            params = {'message' : 'Username should not contain specail characters!!!...'}
            return render(request , 'blog/register.html' , params)


        # user create
        myUser = User.objects.create_user(username , email , pass1)
        myUser.save()
        user = authenticate(username = username , password = pass1)
        if user is not None:
                login(request , user)

        params = {'message' : 'Account has been created successfully!!!..'}
        return redirect('/' , params) 

    else:
        return render(request , 'blog/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password)
        if user is not None:
                login(request , user)
                params = {'message' : 'Account has been logged in successfully!!!..'}
                return redirect('/' , params)
        else:
            params = {'message' : 'Invalid login credentials'}
            return render(request , 'blog/login.html' , params)

    else:
        return render(request , 'blog/login.html')

def addblog(request):
    if(str(request.user)=='AnonymousUser'):
        params = {'message' : 'You have to first logged in to your account to add blog!!!...'}
        return render(request , 'blog/index.html' , params) 

    return render(request , 'blog/addblog.html')



def logout_user(request):
    logout(request)
    params = {'message' : 'You are logged out successfully!!!...'}
    return redirect('/' , params)

def blogpost(request , slug):
    post = Post.objects.filter(slug = slug).first()
    comments = BlogComment.objects.filter(post = post , parent = None)
    replies = BlogComment.objects.filter(post = post).exclude( parent = None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post , 'comments' : comments , 'count' : len(comments) , 'replyDict' : replyDict}
    return render(request , 'blog/blogpost.html' , context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment = comment , user = user , post=post)
            messages.success(request, "Your comment has been posted successfully")

        else:
            parent = BlogComment.objects.get(sno = parentSno)
            comment = BlogComment(comment = comment , user = user , post=post , parent = parent)
            messages.success(request, "Your reply has been posted successfully")
        comment.save()
        
        return redirect(f'/blog/blogs/{post.slug}')

def myblog(request):
    if request.method == 'POST' and request.FILES['image']:
        title = request.POST.get('title')
        category = request.POST.get('category')
        upload = request.FILES.get('image')
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        content = request.POST.get('content')
        usertemp = str(request.user)
        s = slug(usertemp)
        addblog = Post(title = title , catagory = category , content = content , author = request.user ,slug = s, image = file)
        addblog.save()
        return redirect("/blog/blogs/" + s)

    allposts = Post.objects.filter(author = request.user)
    context = {'allposts' : allposts}
    return render(request , 'blog/myblog.html' , context)

def slug(usertemp):
    blog = Post.objects.filter(author = usertemp)
    length = len(blog)
    return usertemp + str(length+2)