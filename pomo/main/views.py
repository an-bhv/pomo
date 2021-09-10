from django.db.models.aggregates import Count
from django.shortcuts import  render, redirect
from requests.api import post
from .forms import NewUserForm,MainForm,SearchForm,CommentForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from . import getit, search
from .models import Item,Myuser,Like
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

	
	

def homepage(request):
	if request.method=="POST":
		form = SearchForm(request.POST)
		if form.is_valid():
#be careful here, this part is to be shifted to other view
				

			return redirect("main:search_res")







	form = SearchForm()
	

	its = Item.objects.annotate(cnt = Count('liked')).order_by('-cnt') 
	user = request.user


	
	return render(request=request, template_name='main/homepage.html',context={'form':form,'items':its,'user':user})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():


			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')

			if(Myuser.objects.filter(email=email).exists()):	
				messages.error(request, "Email already exists.")


			else:
				us = Myuser(email=email,username = username)
				us.save()
			

				user = form.save()

				login(request, user)
				messages.success(request, "Registration successful." )
				return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="main/register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")




def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("main:homepage")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})



@login_required
def like_post(request):
	user = request.user

	if request.method=='POST':
		item_id = request.POST.get('item_id')

		item_obj = Item.objects.get(id=item_id)

		if user in item_obj.liked.all():
			item_obj.liked.remove(user)

		else:
			item_obj.liked.add(user)


		like, created = Like.objects.get_or_create(user=user,item_id=item_id)


		if not created:
			if like.value=='Like':
				like.value='Unlike'
			else:
				like.value='Like'

		like.save()

	return redirect('main:homepage')




@login_required
def delw(request):
	user = Myuser.objects.filter(username = request.user.username)[0]
	if request.method=='POST':
		b = request.POST.get('delw')

		i = user.watched.filter(id=b)[0]

		user.watched.remove(i)

		user.save()

	
	return redirect('main:profile')



@login_required
def deln(request):
	user = Myuser.objects.filter(username = request.user.username)[0]
	if request.method=='POST':
		b = request.POST.get('deln')

		i = user.item.filter(id=b)[0]

		user.item.remove(i)

		user.save()

	
	return redirect('main:profile')






@login_required
def search_res(request):
	usern = request.user.username

	if request.method=='POST':
		imdb_id = request.POST.get('imdb_id')
		
		d = getit.fetch(imdb_id)
		it = Item
		if Item.objects.filter(imdb_id=imdb_id).exists():
			it = Item.objects.filter(imdb_id=imdb_id)[0]
		else:
			it = Item(title=d['title'],year=d['year'],genre=d['genre'],runtime = d['runtime'],released = d['released'],cast = d['cast'],plot = d['plot'], country = d['country'], poster_link = d['poster_link'], metascore = d['metascore'],imdbRating=d['imdbRating'],type=d['type'],imdb_id=d['imdb_id']) 
			it.save()


		if(Myuser.objects.filter(username = usern ).exists()):			
			us = Myuser.objects.filter(username=usern)[0]
		else:
			us = Myuser(email=request.user.email,username = usern)
			us.save()

	

		us.item.add(it)



		return redirect("main:homepage")

	else:
		
		title = request.GET.get('tit')
		
		d,n,res = search.fetch(title)

		if res==False:
			messages.error(request,"No result found")
			return redirect("main:homepage")

		lis = zip(d['title'],d['year'],d['poster_link'],d['type'],d['imdb_id'])
		
		d['lis'] = lis            

		return render(request,template_name="main/search_res.html",context=d)
		
	
@login_required
def profile(request):

	username = request.user.username
	user = Myuser.objects.get(username=username)
	not_watched = user.item.all()
	watched = user.watched.all()
	
	if request.method=='POST':


		for i in not_watched:

			b = request.POST.get(str(i.id))
			if b=='True':
				user.item.remove(i)
				user.watched.add(i)
				user.save()


		for j in watched:
			b = request.POST.get(str(j.id))

			if b=='False':
				user.watched.remove(j)
				user.item.add(j)
				user.save()

		return redirect('main:profile')





			
	
	
	return render(request,template_name='main/profile.html',context={'not_watched':not_watched,'watched':watched,})




@login_required
def post_detail(request):
	it_id = request.GET.get('it_id')
	post = get_object_or_404(Item, id=it_id)
	comments = post.comments.all()
	new_comment = None
    # Comment posted
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
    
		if comment_form.is_valid():

			new_comment = comment_form.save(commit=False)
			itt_id = request.POST.get('itt_id')
			post = get_object_or_404(Item,id=itt_id)
			new_comment.post = post
			new_comment.email = request.user.email
			new_comment.name = request.user.username
			new_comment.save()
			
		
	else:
		comment_form = CommentForm()
	template_name='main/post_detail.html'
	
	return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

