from urllib import quote_plus
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
import posts
from  posts import forms
from forms import PostForm
from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


# Create your views here.
def post_create(request):

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user 
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	#if request.method == 'POST':
		#print request.POST
	context = {"form":form,}
	return render(request,"post_form.html", context)

def post_detail(request, id=None): #retrieve
	instance = get_object_or_404(Post ,id =id)
	share_string = quote_plus(instance.content)
	context = {'title': instance.title, 'instance':instance ,'share_string':share_string}
	return render(request,"post_detail.html", context)

def post_list(request, id =None):
	queryset_list = Post.objects.all().order_by("-timestamp")

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
		Q(title__icontains = query)|
		Q(content__icontains = query)|
		Q(user__first_name__icontains = query)|
		Q(user__last_name__icontains = query)
		).distinct()

	paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
	page = request.GET.get('page')
    
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = { "object_list" : queryset, "title": "list",}
	return render(request,"post_list.html", context)


def post_update(request,id=None):
	instance = get_object_or_404(Post ,id = id)
	form = PostForm(request.POST ,request.FILES or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request,"<a href= '#' >Item</a> Saved", extra_tags='html_safe')


	context = {'title': instance.title, 
		'instance':instance , 
		"form":form,}


	
	return render(request,"post_form.html", context)

def post_delete(request, id=None):
	instance = get_object_or_404(Post ,id = id)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect('posts:list')