#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render, reverse
import json
import collections
import datetime
from content.models import ZbxContent
from django.conf import settings
from content.models import Content, Type, Project

def index(request):
    request.breadcrumbs((('首页', '/'), ('故障列表', reverse('fms_list')), ('故障统计', reverse('cus_dashboard_index'))))
    return render_to_response('dashboard/zbx_index.html', {'request': request})

def zbx_line(request):
    request.breadcrumbs((('首页', '/'), ('故障列表', reverse('fms_list')), ('故障统计', reverse('cus_dashboard_index'))))
    return render_to_response('dashboard/zbx_line.html', {'request': request})

def zbx_bar(request):
    request.breadcrumbs((('首页', '/'), ('故障列表', reverse('fms_list')), ('故障统计', reverse('cus_dashboard_index'))))
    return render_to_response('dashboard/zbx_bar.html', {'request': request})


def get_verbose_name(field):

    data = {}
    params = [v for v in ZbxContent._meta.fields]
    for msg in params:
        data[msg.name] = msg.verbose_name
    verbose_name = data[field]
    return verbose_name



def get_current_month():
    """ 获取首月分至当前所有月份
        print(get_current_month())
        ['2020-01', '2020-02', '2020-03']
    """
    year_month = []
    now_month = datetime.datetime.now().month
    for i in range(1,now_month+1):
       delta = (now_month - i)*365/12
       year_month.append((datetime.date.today() - datetime.timedelta(delta)).strftime("%Y-%m"))
    return year_month


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
    item_data = []
    item_legend = []
    for i in data:
        item_data.append({"name": i.item, "value": i.count})
        item_legend.append(i.item)

    item_text = get_verbose_name(item)
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


def get_line_data(data):

    item_legend = []
    result = {}
    item_data = []
    _tmp = {}
    _data = collections.OrderedDict()
    now_month = datetime.datetime.now().month

    xaxis_month = get_month()

    for d in data:
        _tmp[d.date] = d.count
    for x in xaxis_month:
        if x in _tmp.keys():
            _data[x] = _tmp[x]
        else:
            _data[x] = 0

    item = {"name": '计数', "stack": '总量', "data": list(_data.values()), "type": 'line'}
    result = {"text": '今年故障统计数据', "subtext": 'From Zabbix', "data": item, "legend": item_legend, "xaxis_data": xaxis_month, "type": 'line'}
    return result



def get_month_data():
    data = {}
    data_x = ['一月','二月','三月','四月','五月','六月',
              '七月','八月','九月','十月','十一月','十二月']
    
    # 全年故障统计 
    total_data_y = [Content.objects.filter(start_time__month=d).count() 
                    for d in range(1, 13)] 
     
    total = {'name_total':'故障总数','title_total':'2019年度 故障总数统计',
             'data_x':data_x,'total_data_y':total_data_y}
    
    data.update(total)

    # 影响项目 project = ['值班系统', '安防系统', '文电系统', '视频系统']
    names = Project.objects.values_list('name', flat=True) 
        
    items = []
    for name in names:        
        mylist = []
        for d in range(1, 13):
            mylist.append(Content.objects.filter(start_time__month=d, 
            project=Project.objects.get(name=name)).count())
        items.append(mylist)
         
    title_2019 = '2019年度各分系统故障统计 %s'%'/'.join(names)
    name_0 = names[0]   
    value_0 = items[0]

    name_1 = names[1]   
    value_1 = items[1]

    name_2 = names[2]   
    value_2 = items[2]

    name_3 = names[3]   
    value_3 = items[3]
    
    data.update({'title_2019':title_2019,'legend_data':list(names),
                 'name_0':name_0, 'value_0':value_0,
                 'name_1':name_1, 'value_1':value_1,
                 'name_2':name_2, 'value_2':value_2,
                 'name_3':name_3, 'value_3':value_3,
                 })    

    return data


def zbx_data_line(request):    
    data = get_month_data()
    data.update({'type':'line'})      
    return HttpResponse(json.dumps(data))

def zbx_data_bar(request):    
    data = get_month_data()
    data.update({'type':'bar'})
     
    return HttpResponse(json.dumps(data))











"""
def index_data(request):

    data = {}
    items_pie = ['level', 'type', 'project', 'host']
    items_line = 'fms_sum'

    # 最近三个月数据
    for i in items_pie:
        
        _content = ZbxContent.objects.raw('SELECT id,%s as item,count(id) as count FROM content_zbxcontent WHERE DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(start_time) GROUP BY %s' % (i, i))
        #获取到top10的故障服务器
        if i=='host':
            content = ZbxContent.objects.raw('select * from (SELECT id,%s as item,count(id) as count FROM content_zbxcontent WHERE DATE_SUB(CURDATE(), INTERVAL 3 MONTH) <= date(start_time) GROUP BY %s) a order by count desc' % (i, i))
            _content = content[:10] if content else []
        data[i] = get_pie_data(_content, i)

    # 根据故障项目分类，今年故障数量统计
    content_history = ZbxContent.objects.raw(
        'SELECT id,count(*) as count,DATE_FORMAT(start_time,"%%Y-%%m") as date from content_zbxcontent where YEAR(start_time) = YEAR(CURDATE()) GROUP  by DATE_FORMAT(start_time,"%%Y-%%m")')

    data['fms_sum'] = get_line_data(content_history)

    project = ZbxContent.objects.values_list('project').distinct()
    data['project_item'] = [i[0] for i in project] if project else []
    return HttpResponse(json.dumps(data))


# def select_data(request):

#     data = {}
#     history = ['fms_type_history']

#     if request.method == "POST":
#         if request.POST.get('type') == "project":
#             project = request.POST.get('selected')
#             if project == "All":
#                 sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE())  GROUP BY type_id"
#             else:
#                 project_id = Project.objects.filter(name=project).values('id')[0]['id']
#                 sql = "SELECT b.id,count(*) as count,b.name as name FROM fms.content_content as a  LEFT JOIN content_type as b on a.type_id=b.id  WHERE YEAR(ctime)=YEAR(CURDATE()) and project_id=%s GROUP BY type_id" % project_id
#             content_history = ZbxContent.objects.raw(sql)
#             for k in history:
#                 data[k] = get_pie_history_data(content_history, k)
#         return HttpResponse(json.dumps(data))
#     else:
#         return HttpResponseRedirect('/')
"""