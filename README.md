OMFMS(Operation Maintenance Fault Management System: 运维故障管理系统)
=====================================================================
关键词：重写用户模型 数据可视化 邮件 ajax 前后端分享 Form Page
[![Build Status](https://img.shields.io/travis/geekwolf/fms.svg?branch=master)](https://img.shields.io/travis/geekwolf/fms.svg)

### run
```
运行：    $ ./start.sh
初始化：  $ ./start.sh -i
问题咨询：微信-13402553918  邮箱-wuchunlongcom@outlook.com  
```

### 解决BUG问题记录
```
1、版本升级python375；
2、重写用户模型；
3、'django.middleware.csrf.CsrfViewMiddleware', 取消屏蔽；
4、重写数据可视化模块；
5、解决页面加载时间长；

```


> OMFMS现有功能:

- 故障管理
- 用户管理
- 邮件管理。将故障信息发送短信给维修人员；
- 故障数据统计,数据可视化
- 关于权限：区分超级管理员、普通用户
- 写在最后。自己写用户、组、权限还是复杂，使用DJANGO自己的ADMIN后台，方便！
- 资料：https://github.com/geekwolf/fms
