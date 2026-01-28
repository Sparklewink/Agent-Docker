FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# 安装基础依赖
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 创建普通用户
RUN useradd -ms /bin/bash appuser

#创建数据目录
RUN mkdir -p /app/data

# 复制依赖和代码
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# 赋予 appuser 对整个 /app (包括 data) 的权限
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 4 app:app
