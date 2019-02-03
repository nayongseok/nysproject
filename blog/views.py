from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth import (login as django_login, logout as django_logout, authenticate )# 추가
from .forms import PostForm, CommentForm, LoginForm # 추가
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy


@login_required
def post_read(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()
    return render(request,'blog/post_read.html',{'post':post,'comment_form':comment_form})

@login_required
def add_comment_to_post(request, post_id):
    post=get_object_or_404(Post, id=post_id)
    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect('post_read', post_id = post.pk)

def post_list(request):
    posts = Post.objects.all()
    return render(request,'blog/post_list.html',{'list':posts})

#class MyListView(ListView):
#    model = Post
#    context_object_name = 'list'



@login_required
def post_form(request):
    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_read', post_id = post.pk) #rediredct는 ()안에 URL을 쓰고, 외부 URL을 쓸 수 있다.
    else:
        form=PostForm()
    return render(request,'blog/post_form.html',{'form':form})  # 3번째 값을 만들어서 2번째 html파일에서 사용할 떄

@login_required
def post_edit(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():     #값을 받으면
            post =form.save(commit=False)     # 대신 저장은 하지 않음  
            post.save()  # 객체가 가진 데이터 를저장
            return redirect('post_read', post_id =post.pk) # post.pk가 저장된 곳은 post.id라는 필드이다.
    else:
        form = PostForm(instance=post)  # 포스트 아니면 전처럼 폼을 렌더링하는 것
    return render(request, 'blog/post_edit.html',{'form':form})
    
@login_required
def post_delete(request, post_id):
    post = Post.objects.get(id = post_id)
    if post.author.username ==  request.user.username: 
        post.delete()
        return redirect('post_list')
    else:   
        print(post.author)
        print(type(post.author))
        print(request.user.username)
        print(type(request.user.username))
        print('fail to delete')

def about(request):
    return render(request, 'blog/about.html')

def like(request):
    return render(request, 'blog/like.html')

def hate(request):
    return render(request, 'blog/hate.html')

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('post_read', post_id=comment.post.pk)

def login(request):                                    #추가
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 가져온 username과 password에 해당하는 User가 있는지 판단한다
            # 존재할경우 user변수에는 User인스턴스가 할당되며,
            # 존재하지 않으면 None이 할당된다
            user = authenticate(
                username=username,
                password=password
            )
            # 인증에 성공했을 경우
            if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)
                # Post목록 화면으로 이동
                return redirect('post_list')
            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'blog/login.html', context)

def logout(request):
    django_logout(request)
    return redirect('post_list')

def permission_denied(request):
    return render(request, 'blog/permission_denied.html',{
    })

class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
    template_name = 'blog/signup.html' # 템플릿은?
    form_class =  CreateUserForm # 푸슨 폼 사용? >> 내장 회원가입 폼을 커스터마지징 한 것을 사용하는 경우
    # form_class = UserCreationForm >> 내장 회원가입 폼 사용하는 경우
    success_url = reverse_lazy('post_list') # 성공하면 어디로?