echo '正在搭建IP代理池服务'
pre_dir=$(dirname $(pwd))
docker-compose -f $pre_dir/docker-compose.yml up -d
