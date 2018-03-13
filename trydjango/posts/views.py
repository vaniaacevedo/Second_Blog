from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.db.models import Q

# Create your views here.


def post_create(request):
	form= PostForm(request.POST or None, request.FILES or None) #initialization
	if form.is_valid():
		instance= form.save(commit=False)
		instance.save()
		#messages success
		messages.success(request, 'Successfully Created')
		return HttpResponseRedirect(instance.get_absolute_url())
	context= { 'form':form, }
	return render(request, 'post_form.html', context)

def post_detail(request, id):
	instance= get_object_or_404(Post, id=id)
	context={ 'title': instance.title, 'instance':instance, }
	return render(request, 'post_detail.html', context)

def post_list(request):
	queryset_list= Post.objects.all() #.order_by('-timestamp')
	query=request.GET.get('q')
	if query:
		queryset_list= queryset_list.filter(
			Q(content__icontains=query)|
			Q(title__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			)
	paginator= Paginator(queryset_list, 5)
	page_request_var= 'page'
	page= request.GET.get(page_request_var)
	try:
		queryset= paginator.page(page)
	except PageNotAnInteger:
		#if page is not an integer, deliver first page
		queryset= paginator.page(1)
		#ig page is out of range(e.g.9999), deliver last page of results
	except EmptyPage:
		contacts=paginator.page(paginator.num_pages)
		
	context= { 'title':'Welcome to our blog!','object_list':queryset, 
	'page_request_var':page_request_var }
	return render(request, 'post_list.html', context)

def post_update(request, id=None):
	instance= get_object_or_404(Post, id=id)
	form= PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance= form.save(commit=False)
		instance.save()
		messages.success(request, '<a href="#">Item</a> Saved', extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context= { 'title': instance.title, 'instance': instance, 'form': form, }	
	return render( request, 'post_form.html', context )
	

def post_delete(request, id=None):
	instance= get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, 'Successfully deleted')
	return redirect('posts:list')


