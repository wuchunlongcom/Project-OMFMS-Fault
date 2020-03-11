#-*- coding: utf-8 -*-

from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from commons.paginator import paginator
from content.models import Content
from django.db.models import Q

def fms_search(request):

    data = {}
    search = request.GET.get("search")
    content = Content.objects.filter(Q(title__icontains=search) | Q(type__name__icontains=search) | Q(project__name__icontains=search))
    data = paginator(request, content)
    return render(request, 'fms/fms_table.html',data)