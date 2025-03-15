# 紫微斗数 API 文档

## 基础信息

- **API 地址**: `http://localhost:8000`
- **版本**: 1.0.0
- **描述**: 基于 py-iztro 库的紫微斗数计算 API 服务

## 接口列表

### 1. 根路径

- **URL**: `/`
- **方法**: GET
- **描述**: 返回欢迎信息
- **响应示例**:
  ```json
  {
    "message": "欢迎使用紫微斗数API服务"
  }
  ```

### 2. 通过阳历获取星盘信息 (POST)

- **URL**: `/api/astro/by_solar`
- **方法**: POST
- **描述**: 通过阳历日期、时辰和性别计算紫微斗数星盘
- **请求体**:
  ```json
  {
    "solar_date": "2000-8-16",
    "time_index": 2,
    "gender": "女",
    "fix_leap": true,
    "language": "zh-CN"
  }
  ```
- **参数说明**:
    - `solar_date`: 阳历日期，格式为 YYYY-M-D
    - `time_index`: 出生时辰序号（0-12），0为早子时，1为丑时，依此类推
    - `gender`: 性别，"男"或"女"
    - `fix_leap`: 是否调整闰月情况，默认为 true
    - `language`: 输出语言，默认为 "zh-CN"

### 3. 通过阳历获取星盘信息 (GET)

- **URL**: `/api/astro/by_solar`
- **方法**: GET
- **描述**: 通过阳历日期、时辰和性别计算紫微斗数星盘
- **参数**:
    - `solar_date`: 阳历日期，格式为 YYYY-M-D
    - `time_index`: 出生时辰序号（0-12）
    - `gender`: 性别，"男"或"女"
    - `fix_leap` (可选): 是否调整闰月情况，默认为 true
    - `language` (可选): 输出语言，默认为 "zh-CN"

- **示例**:
  ```
  http://localhost:8000/api/astro/by_solar?solar_date=2000-8-16&time_index=2&gender=女
  ```

### 4. 通过阳历获取大限流年信息 (POST)

- **URL**: `/api/astro/horoscope`
- **方法**: POST
- **描述**: 通过阳历日期、时辰、性别和目标日期计算大限流年信息
- **请求体**:
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
- **参数说明**:
    - `solar_date`: 阳历日期，格式为 YYYY-M-D
    - `time_index`: 出生时辰序号（0-12），0为早子时，1为丑时，依此类推
    - `gender`: 性别，"男"或"女"
    - `target_date`: 目标日期，格式为 YYYY-M-D
    - `fix_leap`: 是否调整闰月情况，默认为 true
    - `language`: 输出语言，默认为 "zh-CN"

### 5. 通过阳历获取大限流年信息 (GET)

- **URL**: `/api/astro/horoscope`
- **方法**: GET
- **描述**: 通过阳历日期、时辰、性别和目标日期计算大限流年信息
- **参数**:
    - `solar_date`: 阳历日期，格式为 YYYY-M-D
    - `time_index`: 出生时辰序号（0-12）
    - `gender`: 性别，"男"或"女"
    - `target_date`: 目标日期，格式为 YYYY-M-D
    - `fix_leap` (可选): 是否调整闰月情况，默认为 true
    - `language` (可选): 输出语言，默认为 "zh-CN"

- **示例**:
  ```
  http://localhost:8000/api/astro/horoscope?solar_date=2000-8-16&time_index=2&gender=女&target_date=2025-01-01
  ```

## 响应数据结构

### 1. 星盘信息响应

API 返回的是星盘信息的 JSON 对象，以下是详细的数据结构说明：

#### 顶层结构

| 字段名 | 类型 | 说明 |
|-------|------|------|
| gender | String | 性别（"男"或"女"） |
| solarDate | String | 阳历日期（如"2000-8-16"） |
| lunarDate | String | 农历日期（如"二〇〇〇年七月十七"） |
| chineseDate | String | 中国传统干支历法日期（天干地支） |
| time | String | 时辰（如"寅时"） |
| timeRange | String | 时间范围（如"03:00~05:00"） |
| sign | String | 星座（如"狮子座"） |
| zodiac | String | 生肖（如"龙"） |
| earthlyBranchOfSoulPalace | String | 命宫地支（如"午"） |
| earthlyBranchOfBodyPalace | String | 身宫地支（如"戌"） |
| soul | String | 命主星（如"破军"） |
| body | String | 身主星（如"文昌"） |
| fiveElementsClass | String | 五行局（如"木三局"） |
| palaces | Array | 十二宫位信息数组 |

#### 宫位结构 (palaces 数组的每个元素)

| 字段名 | 类型 | 说明 |
|-------|------|------|
| index | Number | 宫位索引（0-11）|
| name | String | 宫位名称（如"财帛"、"子女"等）|
| isBodyPalace | Boolean | 是否为身宫 |
| isOriginalPalace | Boolean | 是否为本宫 |
| heavenlyStem | String | 宫位天干（如"甲"、"乙"等）|
| earthlyBranch | String | 宫位地支（如"子"、"丑"等）|
| majorStars | Array | 主星数组 |
| minorStars | Array | 辅星数组 |
| adjectiveStars | Array | 杂耀数组 |
| changsheng12 | String | 长生十二神（如"长生"、"沐浴"等）|
| boshi12 | String | 博士十二神（如"博士"、"力士"等）|
| jiangqian12 | String | 将前十二神（如"将星"、"攀鞍"等）|
| suiqian12 | String | 岁前十二神（如"岁建"、"晦气"等）|
| decadal | Object | 大限信息 |
| ages | Array | 流年年龄数组 |

#### 星曜结构 (majorStars, minorStars, adjectiveStars 数组的每个元素)

| 字段名 | 类型 | 说明 |
|-------|------|------|
| name | String | 星曜名称（如"紫微"、"天府"等）|
| type | String | 星曜类型（major: 主星, soft: 吉星, tough: 煞星, adjective: 杂耀, flower: 桃花星, helper: 解神, lucun: 禄存, tianma: 天马）|
| scope | String | 作用范围（origin: 本命盘）|
| brightness | String | 星曜亮度（庙、旺、得、利、平、不、陷等，可能为空）|
| mutagen | String/null | 四化信息（禄、权、科、忌等，可能为空或null）|

#### 大限结构 (decadal)

| 字段名 | 类型 | 说明 |
|-------|------|------|
| range | Array | 大限起止年龄 [起始年龄, 截止年龄] |
| heavenlyStem | String | 大限天干 |
| earthlyBranch | String | 大限地支 |

### 2. 大限流年信息响应

大限流年接口返回的是包含本命盘和大限流年信息的 JSON 对象：

```json
{
  "natal_chart": {
    // 本命盘信息，结构同上
  },
  "horoscope": {
    "lunarDate": "二〇二四年腊月初二",
    "solarDate": "2025-1-1",
    "decadal": {
      "index": 2,
      "name": "大限",
      "heavenlyStem": "庚",
      "earthlyBranch": "辰",
      "palaceNames": ["夫妻","兄弟","命宫","父母","福德","田宅","官禄","仆役","迁移","疾厄","财帛","子女"],
      "mutagen": ["太阳","武曲","太阴","天同"],
      "stars": [[{"name":"运马","type":"tianma","scope":"decadal","brightness":null,"mutagen":null}]]
    },
    "age": {
      "index": 8,
      "name": "小限",
      "heavenlyStem": "丙",
      "earthlyBranch": "戌",
      "palaceNames": ["官禄","仆役","迁移","疾厄","财帛","子女","夫妻","兄弟","命宫","父母","福德","田宅"],
      "mutagen": ["天同","天机","文昌","廉贞"],
      "stars": [],
      "nominalAge": 25
    },
    "yearly": {
      "index": 2,
      "name": "流年",
      "heavenlyStem": "甲",
      "earthlyBranch": "辰",
      "palaceNames": ["夫妻","兄弟","命宫","父母","福德","田宅","官禄","仆役","迁移","疾厄","财帛","子女"],
      "mutagen": ["廉贞","破军","武曲","太阳"],
      "stars": [[{"name":"流禄","type":"lucun","scope":"yearly","brightness":null,"mutagen":null}]],
      "yearlyDecStar": {
        "jiangqian12": ["岁驿","息神","华盖","劫煞","灾煞","天煞","指背","咸池","月煞","亡神","将星","攀鞍"],
        "suiqian12": ["吊客","病符","岁建","晦气","丧门","贯索","官符","小耗","大耗","龙德","白虎","天德"]
      }
    },
    "monthly": {
      "index": 8,
      "name": "流月",
      "heavenlyStem": "丙",
      "earthlyBranch": "子",
      "palaceNames": ["官禄","仆役","迁移","疾厄","财帛","子女","夫妻","兄弟","命宫","父母","福德","田宅"],
      "mutagen": ["天同","天机","文昌","廉贞"],
      "stars": [[{"name":"yuema","type":"tianma","scope":"monthly","brightness":null,"mutagen":null}]]
    },
    "daily": {
      "index": 9,
      "name": "流日",
      "heavenlyStem": "庚",
      "earthlyBranch": "午",
      "palaceNames": ["田宅","官禄","仆役","迁移","疾厄","财帛","子女","夫妻","兄弟","命宫","父母","福德"],
      "mutagen": ["太阳","武曲","太阴","天同"],
      "stars": [[{"name":"riqu","type":"soft","scope":"daily","brightness":null,"mutagen":null}]]
    },
    "hourly": {
      "index": 9,
      "name": "流时",
      "heavenlyStem": "丙",
      "earthlyBranch": "子",
      "palaceNames": ["田宅","官禄","仆役","迁移","疾厄","财帛","子女","夫妻","兄弟","命宫","父母","福德"],
      "mutagen": ["天同","天机","文昌","廉贞"],
      "stars": [[{"name":"shima","type":"tianma","scope":"hourly","brightness":null,"mutagen":null}]]
    }
  }
}
```

#### 大限流年信息结构说明

1. **顶层结构**
    - `lunarDate`: 农历日期
    - `solarDate`: 阳历日期

2. **大限信息 (decadal)**
    - `index`: 所在宫位的索引
    - `name`: 运限名称（"大限"）
    - `heavenlyStem`: 该运限天干
    - `earthlyBranch`: 该运限地支
    - `palaceNames`: 该运限的十二宫名称数组
    - `mutagen`: 四化星数组
    - `stars`: 流耀数组，每个元素是一个星耀数组

3. **小限信息 (age)**
    - 继承大限信息的所有字段
    - `nominalAge`: 虚岁

4. **流年信息 (yearly)**
    - 继承大限信息的所有字段
    - `yearlyDecStar`: 流年十二神信息
        - `jiangqian12`: 将前十二神数组
        - `suiqian12`: 岁前十二神数组

5. **流月信息 (monthly)**
    - 继承大限信息的所有字段

6. **流日信息 (daily)**
    - 继承大限信息的所有字段

7. **流时信息 (hourly)**
    - 继承大限信息的所有字段

8. **星耀结构**
    - `name`: 星耀名称
    - `type`: 星耀类型（tianma: 天马, soft: 吉星, tough: 煞星, lucun: 禄存, flower: 桃花星等）
    - `scope`: 作用范围（decadal: 大限, yearly: 流年, monthly: 流月, daily: 流日, hourly: 流时）
    - `brightness`: 星耀亮度（可能为 null）
    - `mutagen`: 四化信息（可能为 null）

## 响应示例

### 1. 星盘信息响应示例

```json
{
  "gender": "女",
  "solarDate": "2000-8-16",
  "lunarDate": "二〇〇〇年七月十七",
  "chineseDate": "庚辰 甲申 丙午 庚寅",
  "time": "寅时",
  "timeRange": "03:00~05:00",
  "sign": "狮子座",
  "zodiac": "龙",
  "earthlyBranchOfSoulPalace": "午",
  "earthlyBranchOfBodyPalace": "戌",
  "soul": "破军",
  "body": "文昌",
  "fiveElementsClass": "木三局",
  "palaces": [
    {
      "index": 0,
      "name": "财帛",
      "isBodyPalace": false,
      "isOriginalPalace": false,
      "heavenlyStem": "戊",
      "earthlyBranch": "寅",
      "majorStars": [
        {
          "name": "武曲",
          "type": "major",
          "scope": "origin",
          "brightness": "得",
          "mutagen": "权"
        },
        {
          "name": "天相",
          "type": "major",
          "scope": "origin",
          "brightness": "庙",
          "mutagen": ""
        }
      ]
    }
  ]
}
```

### 2. 大限流年响应示例

```json
{
  "natal_chart": {
    // 本命盘信息，结构同上
  },
  "horoscope": {
    // 大限流年信息，结构同上
  }
}
```

## 错误响应

当API请求出错时，将返回包含错误信息的JSON响应：

```json
{
  "message": "请求参数验证失败",
  "detail": [...] // 详细错误信息
}
```

或

```json
{
  "message": "服务器内部错误: 错误详情"
}
```

## CURL 调用示例

### 1. 获取星盘信息

#### GET 方法

```bash
curl -X GET "http://localhost:8000/api/astro/by_solar?solar_date=2000-8-16&time_index=2&gender=女&fix_leap=true&language=zh-CN" \
  -H "accept: application/json"
```

#### POST 方法

```bash
curl -X POST "http://localhost:8000/api/astro/by_solar" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "solar_date": "2000-8-16",
    "time_index": 2,
    "gender": "女",
    "fix_leap": true,
    "language": "zh-CN"
  }'
```

### 2. 获取大限流年信息

#### GET 方法

```bash
curl -X GET "http://localhost:8000/api/astro/horoscope?solar_date=2000-8-16&time_index=2&gender=女&target_date=2025-01-01&fix_leap=true&language=zh-CN" \
  -H "accept: application/json"
```

#### POST 方法

```bash
curl -X POST "http://localhost:8000/api/astro/horoscope" \
  -H "Content-Type: application/json" \
  -d '{
    "solar_date": "2000-8-16",
    "time_index": 2,
    "gender": "女",
    "target_date": "2025-01-01"
  }'
```

```bash

-- 获取这个月份的天数
curl -X POST "http://localhost:8000/api/calendar/month_days" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{                       
    "date": "2025-03"
  }'
  
```
## 注意事项

1. 时辰索引对照表：
    - 0: 早子时 (23:00-01:00)
    - 1: 丑时 (01:00-03:00)
    - 2: 寅时 (03:00-05:00)
    - 3: 卯时 (05:00-07:00)
    - 4: 辰时 (07:00-09:00)
    - 5: 巳时 (09:00-11:00)
    - 6: 午时 (11:00-13:00)
    - 7: 未时 (13:00-15:00)
    - 8: 申时 (15:00-17:00)
    - 9: 酉时 (17:00-19:00)
    - 10: 戌时 (19:00-21:00)
    - 11: 亥时 (21:00-23:00)
    - 12: 晚子时 (23:00-01:00)

2. API服务支持的语言：
    - "zh-CN": 简体中文
    - "zh-TW": 繁体中文
    - "en-US": 英文
    - "ja-JP": 日文
    - "ko-KR": 韩文
    - "vi-VN": 越南语 
