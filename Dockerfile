# 使用轻量的 Python 镜像
FROM python:3.9-slim

# 设置 python 输出不缓存
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    iproute2 \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 预先创建数据目录
RUN mkdir -p /app/data

# 复制依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制主程序
COPY app.py .

# 暴露端口
EXPOSE 8080

# 启动
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 4 app:app
