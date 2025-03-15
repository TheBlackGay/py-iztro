# 紫微斗数API服务

这是一个基于Node.js版iztro库的紫微斗数计算API服务。该服务提供紫微斗数本命盘和大限流年计算功能。

## 特性

- 基于Node.js iztro库计算紫微斗数
- 稳定计算本命盘和基本的大限流年信息
- FastAPI实现的RESTful API接口
- Docker多平台部署支持
- 单进程运行，性能稳定

## 目录结构

```
.
├── app                   # 应用主目录
│   ├── __init__.py       # 包初始化文件
│   ├── docker_astro.py   # DockerAstro实现类
│   └── main.py           # FastAPI主应用
├── Dockerfile            # Docker构建文件
├── docker-compose.yml    # Docker Compose配置
├── docker-compose.prod.yml # 生产环境Docker Compose配置
├── build_docker.sh       # Docker构建脚本
└── requirements.txt      # Python依赖
```

## 安装与运行

### 本地运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 确保已安装Node.js和npm

3. 运行应用：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker部署

1. 构建Docker镜像：

```bash
./build_docker.sh
```

2. 使用Docker Compose运行：

```bash
docker-compose up -d
```

3. 访问API服务：http://localhost:8000

## API接口说明

### 1. 计算本命盘

**POST /api/astro/by_solar**

请求体：
```json
{
  "solar_date": "2000-8-16",
  "time_index": 2,
  "gender": "女",
  "fix_leap": true,
  "language": "zh-CN"
}
```

**GET /api/astro/by_solar**

参数：
- solar_date: 阳历日期，格式：YYYY-M-D
- time_index: 出生时辰序号，0-12
- gender: 性别，"男"或"女"
- fix_leap: 是否调整闰月，默认为true
- language: 输出语言，默认为"zh-CN"

### 2. 计算大限流年

**POST /api/astro/horoscope**

请求体：
```json
{
  "solar_date": "2000-8-16",
  "time_index": 2,
  "gender": "女",
  "target_date": "2025-01-01",
  "fix_leap": true,
  "language": "zh-CN"
}
```

**GET /api/astro/horoscope**

参数：
- solar_date: 阳历日期，格式：YYYY-M-D
- time_index: 出生时辰序号，0-12
- gender: 性别，"男"或"女"
- target_date: 目标日期，格式：YYYY-M-D
- target_time_index: 目标时辰序号，0-12
- fix_leap: 是否调整闰月，默认为true
- language: 输出语言，默认为"zh-CN"

### 3. 测试API状态

**GET /api/test**

返回API服务状态信息

## 注意事项

由于技术限制，大限流年功能仅提供基本信息（年龄等），不提供完整的详细数据。本服务设计为单进程运行，适合个人或小规模应用使用。
