# -*- coding: utf-8 -*-
#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
BASE_DIR=`pwd -P`
popd > /dev/null

#############
# Functions
#############
function logging {
    echo "[INFO] $*"
}
function build_venv {
    if [ ! -d env ]; then
        virtualenv env
    fi
    . env/bin/activate
    pip3 install -r requirements.txt

}

function del_db {
    logging "Clean"
    rm -rf "db.sqlite3"
    rm -rf "account/migrations/0*.*"
    
}

function creator_db {
    logging "makemigrations" "accounts"
    python "manage.py" "makemigrations" "accounts"

    logging "makemigrations" "content"
    python "manage.py" "makemigrations" "content"


    logging "migrate"
    python "manage.py" "migrate"
    
}

function write_data_db {
    logging "initdb.py"
    python "initdb.py"
}


function launch_webapp {
    python3 "${BASE_DIR}/mysite/manage.py" "runserver" "8000"
}
#############
# Main
#############
cd ${BASE_DIR}
OPT_ENV_FORCE=$1

build_venv

cd ${BASE_DIR}/mysite
#创建数据库表，适合添加数据库后操作，能重复操作，不会破坏数据。
if [ "${OPT_ENV_FORCE}x" == "-cx" ];then    
    creator_db
fi
# 创建数据表、创建超级用户，破坏数据?!!!(2018.01.21)。
if [ "${OPT_ENV_FORCE}x" == "-cax" ];then    
    creator_db
    python3 "${BASE_DIR}/mysite/manage.py" "createsuperuser" #创建超级用户
fi

# 初始化数据库。创建数据表,删除数据后再加载数据。谨慎操作！！！
if [ "${OPT_ENV_FORCE}x" == "-ix" ];then    
    del_db
    creator_db
    write_data_db
fi


launch_webapp
