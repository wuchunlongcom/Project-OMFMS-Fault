#-*- coding: utf-8 -*-

from django.shortcuts import HttpResponseRedirect, HttpResponse, render, reverse
import json
import collections
import datetime
from content.models import Content, Type, Project
from django.conf import settings
from django.http import JsonResponse

fms_level = (
    (0, u"非常严重"),
    (1, u"严重"),
    (2, u"中等"),
    (3, u"一般"),
    (4, u"无影响"),
)

fms_status = (
    (0, u"处理中"),
    (1, u"已恢复"),
    (2, u"改进中"),
    (3, u"已完结"),
)



def index(request):
    """从路由 cus_index_data 获得数据  """
    request.breadcrumbs((('首页', '/'), ('故障列表', reverse('fms_list')), ('故障统计', reverse('cus_dashboard_index'))))
    
    #return render(request, 'dashboard/dashboard_template.html', {'request': request})
    return render(request, 'dashboard/cus_index.html', {'request': request})


def get_verbose_name(field):

    data = {}
    params = [v for v in Content._meta.fields]
    for msg in params:
        data[msg.name] = msg.verbose_name
    verbose_name = data[field]
    return verbose_name

def get_month():
    """ get current year all months  获取当前年度所有月份
    print(get_month())
    ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12']    
    """
    year_month = []
    year = int(datetime.datetime.now().strftime("%Y"))
    year_month = [datetime.date(year, m, 1).strftime('%Y-%m') for m in range(1, 13)]
    return year_month


def get_pie_data(data, item):

    result = {}
    _data = set(data)
    item_data = []
    item_legend = []
    for i in _data:
        item_data.append({"name": i, "value": data.count(i)})
        item_legend.append(i)

    item_text = get_verbose_name(item.split('_')[1])
    result = {"text": item_text, "data": item_data, "legend": item_legend, "subtext": '最近三个月数据', "type": 'pie'}

    return result


def get_pie_history_data(data, item):
    result = {}
    item_data = []
    item_legend = []
    for i in data:
        item_data.append({"name": i.name, "value": i.count})
        item_legend.append(i.name)

    item_text = get_verbose_name(item.split('_')[1])
    result = {"text": item_text, "data": item_data, "legend": item_legend, "subtext": '今年故障统计数据', "type": 'pie'}

    return result


def get_line_data(data, item):

    item_legend = list(data.keys())
    result = {}
    item_data = []
    now_month = datetime.datetime.now().month

    xaxis_month = get_month()
    for k, v in data.items():
        _tmp = collections.OrderedDict()
        for i in xaxis_month:
            if i in list(v.keys()):
                _tmp[i] = v[i]
            else:
                _tmp[i] = 0
        per_item = {"name": k, "stack": '总量', "data": list(_tmp.values()), "type": 'line'}
        item_data.append(per_item)

    text = "今年故障统计"
    if item == "fms_application_sum":
        subtext = "针对业务故障类型"
    elif item == "fms_sum":
        subtext = "针对所有故障类型"
    else:
        pass

    result = {"text": text, "subtext": subtext, "data": item_data, "legend": item_legend, "xaxis_data": xaxis_month, "type": 'line'}

    return result
    
    
def index_data(request):
    data = {}
    
    # 故障类型 type
    names = Type.objects.values_list('name', flat=True)
    count = Content.objects.filter().count()
    legend_data_type = ['%s(%s%%)' %(name, round(Content.objects.filter(
        type=Type.objects.get(name=name)).count()*100/count,2)) 
        for name in names]
     
    series_data_type = [{'value': Content.objects.filter(
        type=Type.objects.get(name=name)).count(),'name':'%s(%s%%)' 
        %(name, round(Content.objects.filter(
        type=Type.objects.get(name=name)).count()*100/count,2)) } 
        for name in names]
    
    type = {'name_type':'故障类型','legend_data_type':legend_data_type, 
            'series_data_type':series_data_type}
    
    data.update(type)
    
    
    # 影响项目 project
    names = Project.objects.values_list('name', flat=True)
    legend_data_project = ['%s(%s%%)' %(name, round(Content.objects.filter(
        project=Project.objects.get(name=name)).count()*100/count,2)) 
        for name in names]

    
    series_data_project = [{'value': Content.objects.filter(
        project=Project.objects.get(name=name)).count(),'name':'%s(%s%%)' 
        %(name, round(Content.objects.filter(
        project=Project.objects.get(name=name)).count()*100/count,2)) } 
        for name in names]
    
    project = {'name_project':'影响项目','legend_data_project':legend_data_project, 
            'series_data_project':series_data_project}
    
    data.update(project)
    
       
    # 故障级别 level   
    legend_data_level = ['%s(%s%%)' %(i[1], round(Content.objects.filter(
        level=i[0]).count()*100/count, 2)) for i in fms_level]  
     
    series_data_level = [{'value': Content.objects.filter(level=i[0]).count(), 
        'name':'%s(%s%%)' %(i[1], round(Content.objects.filter(
        level=i[0]).count()*100/count, 2) ) } for i in fms_level]
    
    level = {'name_level':'故障级别','legend_data_level':legend_data_level, 
            'series_data_level':series_data_level} 
       
    data.update(level)
    
    
    # 故障状态 fms_status
    legend_data_status = ['%s(%s%%)' %(i[1], round(Content.objects.filter(
        status=i[0]).count()*100/count, 2)) for i in fms_status]  
    
    series_data_status = [{'value': Content.objects.filter(status=i[0]).count(), 
        'name':'%s(%s%%)' %(i[1], round(Content.objects.filter(
        status=i[0]).count()*100/count, 2) ) } for i in fms_status]

    status = {'name_status':'故障状态','legend_data_status':legend_data_status, 
            'series_data_status':series_data_status} 
       
    data.update(status)
    
    return HttpResponse(json.dumps(data))

def select_data(request):
    
    if request.method == "POST":    
        data = { "code":10000 }
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseRedirect('/')

"""
def index_data(request):
    
    data = {}
    items_pie = ['fms_level', 'fms_type', 'fms_project']
    history = ['fms_type_history']
    items_line = ['fms_sum', 'fms_application_sum']

    content = Content.objects.raw('SELECT * FROM content_content WHERE DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(ctime)')
    content_history = Content.objects.raw(
        'SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE()) GROUP BY type_id')
    project_list = Project.objects.all()

    # all project list
    project = [i.name for i in project_list]

    print('project=====', project)
    
    fms_level = []
    fms_type = []
    fms_project = []
    fms_type_history = []

    _tmp = {}
    for i in content:
        fms_level.append(i.get_level_display())
        fms_type.append(str(i.type))
        fms_project.append(str(i.project))

    _tmp['fms_level'] = fms_level
    _tmp['fms_type'] = fms_type
    _tmp['fms_project'] = fms_project

    _year_sum = Content.objects.raw(
        'SELECT id,count(*) as count,project_id,DATE_FORMAT(ctime,"%%Y-%%m") as date from content_content where YEAR(ctime) = YEAR(CURDATE()) GROUP  by project_id,DATE_FORMAT(ctime,"%%Y-%%m")')
    # 针对业务故障，查询条件设置成该类型ID
    _year_application_sum = Content.objects.raw(
        'SELECT id,count(*) as count,project_id,DATE_FORMAT(ctime,"%%Y-%%m") as date from content_content where YEAR(ctime) = YEAR(CURDATE()) and type_id in {0} GROUP  by project_id,DATE_FORMAT(ctime,"%%Y-%%m")'.format(tuple(settings.SPECIAL_TYPES)))

    year_sum = collections.defaultdict(dict)
    year_application_sum = collections.defaultdict(dict)

    for i in _year_sum:
        year_sum[str(i.project)][i.date] = i.count

    for i in _year_application_sum:
        year_application_sum[str(i.project)][i.date] = i.count

    for k in items_pie:
        data[k] = get_pie_data(_tmp[k], k)

    for k in items_line:
        if k == "fms_application_sum":
            data[k] = get_line_data(year_application_sum, k)
        else:
            data[k] = get_line_data(year_sum, k)

    for k in history:
        data[k] = get_pie_history_data(content_history, k)
        
    data['project'] = project

    return HttpResponse(json.dumps(data))


def select_data(request):

    data = {}
    history = ['fms_type_history']

    if request.method == "POST":
        if request.POST.get('type') == "project":
            project = request.POST.get('selected')
            if project == "All":
                sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE())  GROUP BY type_id"
            else:
                project_id = Project.objects.filter(name=project).values('id')[0]['id']
                sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE()) and project_id=%s GROUP BY type_id" % project_id
            content_history = Content.objects.raw(sql)
            for k in history:
                data[k] = get_pie_history_data(content_history, k)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseRedirect('/')
"""