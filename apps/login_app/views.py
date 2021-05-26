from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt


# Create your views here.
def logreg(request):
    return render(request, "log_reg.html")

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.hash_pw.encode()):
            request.session['userid'] = logged_user.id
            request.session['username'] = logged_user.first_name
            return redirect('/wall')
    return redirect('/')

'''
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:

        return redirect('/success')
'''
def reg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            hash_pw = pw_hash,
        )
        user = User.objects.last()
        request.session['userid'] = user.id

        return redirect('/wall')

def success(request):
    if request.session['userid']:
        return render(request, "success.html")
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def wall(request):
    messages = Message.objects.all()
    comments = Comment.objects.all()
    #print(messages.users)
    context = {
        'messages': messages,
        'comments': comments
    }
    return render(request, 'wall.html', context)

def post_message(request):
    print(request.session['userid'])
    user = User.objects.get(id=request.session['userid'])
    print(user)
    Message.objects.create(
        user = user,
        message = request.POST['message']
    )
    return redirect ('/wall')

def post_comment(request):
    return redirect ('/wall')