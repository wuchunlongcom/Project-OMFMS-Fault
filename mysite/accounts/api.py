#-*- coding: utf-8 -*-

from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from commons.paginator import paginator
from accounts.models import MyUser
from django.db.models import Q

def user_search(request):

    data = {}
    search = request.GET.get("search")
    user = MyUser.objects.filter(Q(group__name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search) | Q(fullname__icontains=search) | Q(mobile__icontains=search))
    data = paginator(request, user)
    return render(request, 'accounts/user/user_table.html',data)