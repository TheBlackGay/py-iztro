FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js和npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 先复制本地py-iztro-master目录
COPY py-iztro-master /app/py-iztro-master/

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 尝试从本地安装py-iztro，提供多种备选方案
RUN if [ -f "/app/py-iztro-master/setup.py" ] || [ -f "/app/py-iztro-master/pyproject.toml" ]; then \
    echo "使用pip install安装py-iztro" && \
    pip install -e /app/py-iztro-master/; \
  elif [ -d "/app/py-iztro-master/py_iztro" ]; then \
    echo "使用手动复制安装py-iztro" && \
    cp -r /app/py-iztro-master/py_iztro /usr/local/lib/python3.12/site-packages/; \
  else \
    echo "警告：找不到py-iztro模块，使用找到的任何目录" && \
    find /app/py-iztro-master -type d -name "py_iztro" -exec cp -r {} /usr/local/lib/python3.12/site-packages/ \; || \
    echo "未找到py_iztro目录，安装失败"; \
  fi

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app:/app/py-iztro-master
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"] 