# 紫微斗数 API 服务

基于 py-iztro 的紫微斗数计算 API 服务。

## 功能特点

- 提供紫微斗数命盘计算API
- 支持通过阳历日期获取星盘信息
- 支持计算大限流年数据
- 提供GET和POST两种请求方式
- 完善的错误处理和日志记录
- 防崩溃设计，即使底层库出现段错误也能优雅处理
- 支持模拟数据模式，在无法加载py_iztro库时仍能提供基本功能

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python start_service.py
```

或者直接运行main.py：

```bash
python main.py
```

服务将在 `http://0.0.0.0:8000` 上启动。

## 运行模式

### 正常模式
当成功导入py_iztro库时，API将使用该库进行紫微斗数计算，提供完整的功能。

### 模拟数据模式
当无法导入py_iztro库时，API将自动切换到模拟数据模式，提供基本的功能和模拟数据，确保服务仍然可用。

## API 使用

### 1. 通过阳历获取星盘信息（GET 方法）

```
GET /astro/by_solar?solar_date=1990-1-1&time_index=0&gender=男&fix_leap=true&language=zh-CN
```

参数说明：
- `solar_date`: 阳历日期，格式为 YYYY-M-D
- `time_index`: 出生时辰序号，0-12，0为早子时，1为丑时，依此类推
- `gender`: 性别，"男"或"女"
- `fix_leap`: 是否调整闰月情况，默认为 true
- `language`: 输出语言，默认为 "zh-CN"

### 2. 通过阳历获取星盘信息（POST 方法）

```
POST /astro/by_solar
```

请求体示例：
```json
{
  "solar_date": "1990-1-1",
  "time_index": 0,
  "gender": "男",
  "fix_leap": true,
  "language": "zh-CN"
}
```

### 3. 计算大限流年（GET 方法）

```
GET /astro/horoscope?solar_date=1990-1-1&time_index=0&gender=男&target_date=2023-1-1&fix_leap=true&language=zh-CN
```

参数说明：
- `solar_date`: 出生的阳历日期，格式为 YYYY-M-D
- `time_index`: 出生时辰序号，0-12，0为早子时，1为丑时，依此类推
- `gender`: 性别，"男"或"女"
- `target_date`: 目标日期，计算该日期的大限流年，格式为 YYYY-MM-DD
- `fix_leap`: 是否调整闰月情况，默认为 true
- `language`: 输出语言，默认为 "zh-CN"

### 4. 计算大限流年（POST 方法）

```
POST /astro/horoscope
```

请求体示例：
```json
{
  "solar_date": "1990-1-1",
  "time_index": 0,
  "gender": "男",
  "target_date": "2023-1-1",
  "fix_leap": true,
  "language": "zh-CN"
}
```

### 5. 测试接口

```
GET /api/test
```

用于测试API服务是否正常运行，会返回服务状态信息，包括使用的计算类和运行模式。

### 6. 在线API文档

访问 `http://0.0.0.0:8000/docs` 查看交互式API文档。

## 错误处理

所有API都将返回统一的响应格式：

```json
{
  "status": "ok|error|partial",
  "message": "成功或错误信息",
  "timestamp": "ISO格式的时间戳",
  "result": "计算结果（成功时）",
  "error": "详细错误信息（失败时）"
}
```

### 状态说明
- `ok`: 请求完全成功
- `error`: 请求失败
- `partial`: 部分成功（例如：本命盘计算成功但大限流年计算失败）

错误情况下不会返回HTTP 500错误，而是返回200状态码并在响应体中包含错误信息，便于前端处理。

## 防崩溃机制

本API服务实现了多层防崩溃机制：

1. **SIGSEGV信号处理**: 捕获段错误信号，防止服务直接崩溃
2. **安全执行函数**: 所有计算操作都通过安全执行函数调用，提供错误隔离
3. **模拟数据模式**: 当底层库不可用时，提供模拟数据确保服务可用性
4. **部分成功响应**: 当部分计算失败时，仍返回可用的数据 