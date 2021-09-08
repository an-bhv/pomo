from django.shortcuts import  render, redirect
from requests.api import post
from .forms import NewUserForm,MainForm,SearchForm
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

# Create your views here.

	
	

def homepage(request):
	if request.method=="POST":
		form = SearchForm(request.POST)
		if form.is_valid():
#be careful here, this part is to be shifted to other view
				

			return redirect("main:search_res")







	form = SearchForm()
	

	its = Item.objects.all()
	user = request.user


	
	return render(request=request, template_name='main/homepage.html',context={'form':form,'items':its,'user':user})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
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



def search_res(request):
	user_email = request.user.email

	if request.method=='POST':
		imdb_id = request.POST.get('imdb_id')
		
		d = getit.fetch(imdb_id)
		it = Item(title=d['title'],year=d['year'],genre=d['genre'],runtime = d['runtime'],released = d['released'],cast = d['cast'],plot = d['plot'], country = d['country'], poster_link = d['poster_link'], metascore = d['metascore'],imdbRating=d['imdbRating'],type=d['type']) 
	
		it.save()
		if(Myuser.objects.filter(email__exact=user_email).exists()):			
			us = Myuser.objects.filter(email__exact=user_email)[0]
		else:
			us = Myuser(email=user_email)
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

		return render(request,template_name="search_res.html",context=d)
		
	





