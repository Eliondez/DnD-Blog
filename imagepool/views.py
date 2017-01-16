from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from .models import ImagePool

def get_list(request):
    try:
        page_num = request.GET['page']
    except:
        page_num = 1
    paginator = Paginator(ImagePool.objects.filter(user = request.user), 4)
    try:
        page = paginator.page(page_num)
    except:
        page = paginator.page(1)

    output = {}
    output['images'] = []
    for image in page:
        output['images'] = output['images'] + [{'src': image.image.url,
                                                'delete_src': reverse('imagepool:delete_file', kwargs = {'pk': image.pk})}]
    if page.has_previous():
        output['prev_url'] = reverse('imagepool:index') + '?page=' + str(page.previous_page_number())
    else:
        output['prev_url'] = ""
    if page.has_next():
        output['next_url'] = reverse('imagepool:index') + '?page=' + str(page.next_page_number())
    else:
        output['next_url'] = ""
    #print("Got images: ", len(output)-2)
    return JsonResponse(output)


def upload_file(request):
    if request.method == "POST":
        if request.FILES['file_to_upload']:
            image = ImagePool(user = request.user, image = request.FILES['file_to_upload'])
            image.save()
    return HttpResponse('!!!')

def delete_file(request, pk):
    try:
        image = ImagePool.objects.get(pk = pk)
    except:
        return JsonResponse({'status': 0})
    if image.user == request.user:
        try:
            image.delete()
        except:
            return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})
