
from django.shortcuts import render,get_object_or_404,redirect
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from actions.utils import create_action


from .forms import ImageCreateForm

#config redis
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,
						port=settings.REDIS_PORT,
						db=settings.REDIS_DB)



# Create your views here.


@login_required
def image_detail(request,id,slug):
	image = get_object_or_404(Image,pk = id,slug = slug)
	total_views = r.incr('image:{}:views'.format(image.id))
	r.zincrby('image_ranking',image.id,1)
	return render(request,'images/image/detail.html',{"section":'images','image':image,'total_views':total_views})

@login_required
def image_ranking(request):
	image_ranking = r.zrange('image_ranking',0,-1,desc=True)[:10]
	image_ranking_ids = [int(id) for id in image_ranking]
	most_viewed = list(Image.objects.filter(id__in = image_ranking_ids))
	most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
	return render(request,'images/image/ranking.html',
					{'section': 'images',
					'most_viewed': most_viewed})


@login_required
def image_create(request):
	if request.method == "POST":
		form = ImageCreateForm(data = request.POST,files = request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			new_item = form.save(commit = False)
			new_item.user = request.user
			new_item.save()
			create_action(request.user,'upload image',new_item)
			messages.success(request,"Image added successfully")
			return redirect(new_item.get_absolute_url())
	else:
		form = ImageCreateForm()
	return render(request,'images/image/create.html',{"section":'images','form':form})

@ajax_required
@login_required
@require_POST
def image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id = image_id)
			if action == 'like':
				image.users_like.add(request.user)
				create_action(request.user,'like',image)
			else:
				image.users_like.remove(request.user)
			return JsonResponse({'status':'ok'})
		except:
			pass
	return JsonResponse({'status':'ok'})


@login_required
def image_list(request):
	images_list = Image.objects.all()
	paginator = Paginator(images_list,8)
	page = request.GET.get('page')
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse("")
		images = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request,'images/image/list_ajax.html',
			{'section':'images','images':images})
	return render(request,'images/image/list.html',{"section":'images','images':images})



