#-*- coding: utf-8 -*-

from django.shortcuts import render, reverse, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth

from django.contrib.auth.models import Group, Permission
import json
import collections
from django.contrib.auth.decorators import permission_required,login_required,user_passes_test


@login_required
@user_passes_test(lambda u: u.is_superuser)
def permission(request):

    data = collections.defaultdict(list)

    if request.GET.get('id'):
        group = get_object_or_404(Group, id=request.GET.get('id'))
        data['group'] = group
        data['gperm'] = group.permissions.all()
        
    perms = Permission.objects.all()
    for p in perms:
        data[p.content_type.app_label].append(p)

    if request.method == "POST":

        id = request.POST.get('id')
        perms = list(json.loads(request.POST.get('perms')))
        group = get_object_or_404(Group, id=id)

        #perms = Permission.objects.filter(codename__in = perms)
        
        print('perms======', perms)
        #group.permissions.clear()
        #group.permissions.add(*perms)
        
        #return HttpResponse('ok')
    data['request'] = request
    return render(request, 'accounts/user/permission.html', data)
