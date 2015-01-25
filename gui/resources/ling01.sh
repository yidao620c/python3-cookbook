#!/bin/bash

echo '先停止tomcat...'
ps aux |grep tomcat |grep -v 'grep tomcat' |awk '{print $2}'|sudo xargs kill -9
wait

echo '成功停止!开始替换class文件'
cd /usr/local/apache-tomcat-8.0.15/webapps/ROOT/WEB-INF/classes/com
rm -rf winhong/
unzip ling.zip
wait
rm -f ling.zip
echo 'class文件解压替换完成,开始替换配置文件'
cd ..
find . -maxdepth 1 -type f -not -name '*.zip' -print0 | xargs -0 rm
unzip lingconfig.zip
wait
rm -f lingconfig.zip
echo '配置文件解压替换完成'

