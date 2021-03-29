FROM python:3.8

ENV PYTHONUNBUFFERED 1

# 添加目录
ADD . /proxy_pool

# 设置工作目录
WORKDIR /proxy_pool

#设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 更新
#RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r ./requirements.txt

CMD python manager.py