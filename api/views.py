from django.shortcuts import render,get_object_or_404
from datetime import timedelta
from datetime import datetime
from django.http import JsonResponse , HttpResponse
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib.auth.models import User
import re

# function to get ip address
def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

#home page
def home( request):

# Logging system: compare ips if user is authenticated (redirect page when a user registers or logins)
    if request.user.is_authenticated:

       last_ip = request.user.userprofile.ip_address
       current_ip = get_ip(request)

       ip_stat = ""
       if current_ip == last_ip:
          ip_stat = "Safe IP"
       else:
          ip_stat = "Warning: Different IP than usual"
    else:
        ip_stat = get_ip(request)
    #render the html passing ip info
    return render( request, "api/home.html",{"ip_stat": ip_stat})

# posts of last hour page
def posts(request):
    response = []
    #get time now
    this_hour = datetime.now()
    #-1 hour
    one_hour_before = this_hour - timedelta(hours=1)
    #filter posts
    posts = Post.objects.filter(datetime__range=(one_hour_before ,this_hour))

    #building Json response
    for post in posts:
        response.append(
            {
                'title' : post.title,
                'datetime' : post.datetime,
                'content' : post.content,
                'author' : f"{post.user.first_name} {post.user.last_name}",
                'hash' : post.hash,
                'txId': post.txId
            }
        )
    #return Json in the page
    return JsonResponse(response, safe=False)

# function that handles how feed is shown
def post_list(request):

    # filter to show most recent post on top of page
    posts = Post.objects.filter().order_by('-datetime')

   #post form
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.datetime = datetime.now()

            # Uncomment below if you want all posts validated on block chain
            #post.writeOnChain()

            post.save()
            form = PostForm()
        return redirect('/post_list', {'posts': posts, 'form': form})
    else:
        form = PostForm()
        return render(request, 'api/post_list.html', {'posts': posts, 'form': form})

# Analytics page | only superuser can access | passing number of posts
def analytics(response):
    user_posts = User.objects.annotate(total_posts=Count('post'))
    return render(response, "api/analytics.html", {"user_posts": user_posts})

# page /user/<int:id>/ showing some info for each user (try id: 1 , 20 , 21)
def user_id(request,id):
    user = get_object_or_404(User, id=id)
    user_posts = Post.objects.filter(user=user).count()
    return render(request, 'api/user_id.html', {'user': user,"user_posts": user_posts})

# /wordcheck?q=<GET> endpoint check with GET number of times a word is present in posts
def wordcheck(request):
    r = request.GET.get('q','')
    posts = Post.objects.filter().order_by('-datetime')
    resp = 0
    for post in posts:
        print(r)
        wordList = re.sub("[^\w]", " ", post.content).split()
        if post.title == r or r in wordList:
            resp += 1
  # return message on page
    return HttpResponse(f'The word {r} appears {resp} times in all posts')



