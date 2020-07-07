from django.shortcuts import render,HttpResponse,redirect
from .models import BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.
from .models import Post
def blogHome(request):
    allPosts = Post.objects.all()
    return render(request,'blog/blogHome.html',{'allPosts':allPosts})

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    
         
    return render(request,'blog/blogPost.html',{'post':post,'comments':comments,'replies':repDict,'user':request.user})

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        post = Post.objects.get(sno=postSno)
        if parentSno == "":
            blogComment = BlogComment(comment=comment,user=user,post=post)
            blogComment.save()
            messages.success(request,"Comment added successfully..")
            
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            blogComment = BlogComment(comment=comment,user=user,post=post,parent=parent)

            blogComment.save()
            messages.success(request,"Reply added successfully..")
    

    return redirect(f'/blog/{post.slug}')