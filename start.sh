# docker compose 启动命令
#echo 'docker-compose正在启动容器'
#docker-compose up -d

#docker 命令
project_name="ppool"
echo '正在创建项目{'$project_name'}容器'
current_dir=$(pwd)
echo '项目当前路径:'$current_dir
git pull
docker stop $project_name
docker rm $project_name
docker build -t $project_name .
docker run -d -p 5000:5000 -v $current_dir:/$project_name --name $project_name $project_name
docker start $project_name