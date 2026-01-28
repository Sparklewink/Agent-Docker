# 使用轻量的 Python 镜像
FROM python:3.9-slim

# 设置 python 输出不缓存，方便查看日志
ENV PYTHONUNBUFFERED=1

# 安装 curl 和 unzip 依赖
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 创建数据目录
RUN mkdir -p /app/data

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制主程序
COPY app.py .


# 暴露端口
EXPOSE 8080

# 使用 Gunicorn 启动 Flask 应用
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 4 app:app
