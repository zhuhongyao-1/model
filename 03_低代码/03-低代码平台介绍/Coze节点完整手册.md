# Coze 节点完整手册

> 本手册详细介绍 Coze 工作流平台中所有可用节点的功能、配置方法和使用场景。
>
> 更新时间: 2026年3月31日

---

## 目录

1. [节点分类概览](#节点分类概览)
2. [基础节点](#基础节点)
3. [流程控制节点](#流程控制节点)
4. [数据处理节点](#数据处理节点)
5. [AI能力节点](#ai能力节点)
6. [知识库节点](#知识库节点)
7. [数据库节点](#数据库节点)
8. [会话管理节点](#会话管理节点)
9. [消息管理节点](#消息管理节点)
10. [异步处理节点](#异步处理节点)
11. [节点组合最佳实践](#节点组合最佳实践)

---

## 节点分类概览

Coze 平台将节点分为以下几大类:

| 分类 | 主要用途 | 典型节点 |
|------|---------|---------|
| **基础节点** | 工作流的入口和出口 | 输入节点、输出节点 |
| **流程控制节点** | 控制工作流的执行路径 | 条件分支、循环、批处理 |
| **数据处理节点** | 处理和转换数据 | 代码节点、变量赋值、JSON处理 |
| **AI能力节点** | 提供人工智能能力 | 大模型节点、意图识别、问答 |
| **知识库节点** | 存储和检索知识 | 知识库检索、写入、删除 |
| **数据库节点** | 数据持久化存储 | 数据库增删改查 |
| **会话管理节点** | 管理对话会话 | 创建会话、查询会话 |
| **消息管理节点** | 管理对话消息 | 创建消息、查询消息 |
| **异步处理节点** | 后台任务处理 | 异步任务节点 |

---

## 基础节点

### 1. 输入节点 (Input Node)

**作用**: 定义工作流的入口参数,是整个流程的起点。

**配置项**:

```yaml
参数名称: 自定义变量名
参数类型: 
  - String (文本)
  - Number (数字)
  - Boolean (布尔值)
  - Object (对象)
  - Array (数组)
是否必填: 是/否
默认值: 可选
说明: 参数用途描述
```

**使用示例**:

```yaml
参数列表:
  - 参数名: user_message
    类型: String
    必填: 是
    说明: 用户输入的消息内容
    
  - 参数名: user_id
    类型: String
    必填: 是
    说明: 用户唯一标识
    
  - 参数名: session_id
    类型: String
    必填: 否
    默认值: ""
    说明: 会话ID,为空表示新会话
```

**输出变量**: 
- 后续所有节点都可以通过 `{{input.参数名}}` 引用输入值

**关键点**:
- 输入参数是工作流的"原材料"
- 参数类型要选择正确,影响后续节点使用
- 可以为参数设置默认值,提高工作流鲁棒性

---

### 2. 输出节点 (Output Node)

**作用**: 定义工作流最终返回给调用者的数据结构,是流程的终点。

**配置项**:

```yaml
输出字段:
  - 字段名: 自定义输出名
    字段类型: String/Number/Boolean/Object/Array
    值来源: 引用上游节点的变量
```

**使用示例**:

```yaml
输出字段列表:
  - 字段名: reply
    类型: String
    值: "{{final_reply}}"
    说明: 最终回复内容
    
  - 字段名: session_id
    类型: String
    值: "{{session_id}}"
    说明: 会话ID,用于续接
    
  - 字段名: status
    类型: String
    值: "success"
    说明: 处理状态
```

**关键点**:
- 输出节点是工作流的"终点",只能有一个主输出节点
- 输出字段的值必须来自上游节点的变量引用
- 返回的数据结构应该清晰、完整,便于调用方使用

---

## 流程控制节点

### 3. 条件分支节点 (Condition/Branch Node)

**作用**: 根据条件判断,将流程导向不同的分支,类似编程中的 if-else 语句。

**配置项**:

```yaml
分支规则:
  - 分支名: 分支1名称
    条件表达式: 判断条件
    连接到: 目标节点
    
  - 分支名: 分支2名称
    条件表达式: 判断条件
    连接到: 目标节点
    
  - 默认分支: 兜底分支名称
```

**支持的运算符**:

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `==` | 等于 | `intent == "售前"` |
| `!=` | 不等于 | `status != "closed"` |
| `>` | 大于 | `count > 10` |
| `<` | 小于 | `score < 0.6` |
| `>=` | 大于等于 | `age >= 18` |
| `<=` | 小于等于 | `price <= 100` |
| `contains` | 包含 | `message contains "退款"` |
| `is empty` | 为空 | `session_id is empty` |
| `is not empty` | 不为空 | `order_id is not empty` |

**使用示例**:

```yaml
条件分支节点配置:
  分支规则:
    - 分支名: 售前分支
      条件: primary_intent == "售前"
      连接: 售前处理流程
      
    - 分支名: 售后分支
      条件: primary_intent == "售后"
      连接: 售后处理流程
      
    - 分支名: 通用分支
      条件: primary_intent == "通用"
      连接: 通用处理流程
      
    - 默认分支: 其他分支
```

**关键点**:
- 条件按从上到下的顺序判断,满足第一个条件就执行对应分支
- 必须设置默认分支,处理所有未匹配的情况
- 每个分支可以有完全不同的后续节点
- 支持多条件组合 (AND/OR)

---

### 4. 循环节点 (Loop Node)

**作用**: 对数组中的每个元素逐一执行相同的处理逻辑,类似编程中的 for 循环。

**配置项**:

```yaml
循环设置:
  循环来源: 数组变量 (如 {{ticket_list}})
  当前项变量名: 自定义变量名 (如 current_item)
  循环体: 包含的子节点
```

**工作原理**:
1. 从数组中取出一个元素
2. 赋值给"当前项变量名"
3. 执行循环体内的所有节点
4. 重复上述步骤,直到遍历完数组

**使用示例**:

```yaml
循环节点配置:
  循环来源: "{{db_query.ticket_list}}"
  当前项变量名: current_ticket
  
  循环体内节点:
    1. 代码节点: 判断当前工单状态
    2. 条件分支: 根据状态决定是否标记
    
  输出:
    - results_array: 每次循环的结果汇总成新数组
```

**输出变量**:
- `results_array`: 所有循环结果的数组
- `loop_count`: 循环执行次数

**关键点**:
- 循环是串行执行,一个接一个
- 循环体内可以放多个节点
- 注意循环次数,过多会影响性能
- 循环体内可以通过 `{{loop.当前项变量名}}` 引用当前元素

---

### 5. 批处理节点 (Batch Processing Node)

**作用**: 并行处理数组中的多个元素,与循环节点的区别是: 循环是串行,批处理是并行。

**配置项**:

```yaml
批处理设置:
  输入数组: 数组变量
  并发数量: 最大同时处理数
  批处理体: 包含的子节点
```

**使用示例**:

```yaml
批处理节点配置:
  输入数组: "{{warehouse_list}}"
  并发数量: 3
  
  批处理体内节点:
    - HTTP请求节点: 查询当前仓库库存
    
  输出:
    - batch_results: 所有仓库的查询结果数组
```

**关键点**:
- 批处理比循环快,适合独立的并行任务
- 注意设置合理的并发上限,避免触发下游API限流
- 结果顺序可能与输入顺序不一致
- 批处理体内的任务应该是相互独立的

---

### 6. 变量聚合节点 (Variable Aggregator Node)

**作用**: 将多个分支的输出变量合并成统一的变量,供后续节点使用。

**配置项**:

```yaml
聚合规则:
  - 来自分支1: 变量A → 映射到 统一变量X
  - 来自分支2: 变量B → 映射到 统一变量X
  - 来自分支3: 变量C → 映射到 统一变量X
```

**使用示例**:

```yaml
变量聚合节点配置:
  聚合规则:
    # 来自不同分支的相同含义变量,映射到统一名称
    - 来自售前分支: pre_answer → branch_answer
    - 来自售中分支: mid_answer → branch_answer
    - 来自售后分支: after_answer → branch_answer
    - 来自通用分支: general_answer → branch_answer
    
  输出变量:
    - branch_answer: 当前实际执行分支的处理结果
```

**聚合方式**:
- **取第一个非空值**: 按顺序取第一个不为空的值
- **拼接所有值**: 将所有值拼接成一个字符串
- **自定义规则**: 根据业务逻辑自定义

**关键点**:
- 多分支汇聚的必备节点
- 让后续节点可以统一引用变量,不需要判断来源分支
- 聚合时要注意变量的类型一致性

---

## 数据处理节点

### 7. 变量赋值节点 (Variable Assignment Node)

**作用**: 在流程中动态创建或修改变量的值。

**配置项**:

```yaml
赋值操作:
  - 目标变量: 变量名
    赋值来源: 值或表达式
```

**支持的操作**:

| 操作类型 | 说明 | 示例 |
|---------|------|------|
| 固定值赋值 | 直接赋常量 | `status = "processing"` |
| 变量引用 | 引用其他变量 | `answer = {{qa_answer}}` |
| 字符串拼接 | 拼接多个变量 | `case_id = "CS" + {{timestamp}} + {{order_id}}` |
| 条件赋值 | 根据条件赋值 | `priority = {{score}} > 0.9 ? "high" : "normal"` |
| 表达式计算 | 数学或逻辑运算 | `total = {{price}} * {{quantity}}` |

**使用示例**:

```yaml
变量赋值节点配置:
  赋值操作:
    - 目标变量: case_id
      赋值来源: "CS{{timestamp}}{{order_id}}"
      
    - 目标变量: status
      赋值来源: "processing"
      
    - 目标变量: priority
      赋值来源: "{{confidence}} > 0.9 ? 'high' : 'normal'"
```

**关键点**:
- 支持表达式计算和字符串拼接
- 赋值后的变量可被后续任意节点引用
- 与代码节点相比更简单,适合简单的赋值逻辑
- 复杂的数据处理应该使用代码节点

---

### 8. 代码节点 (Code Node)

**作用**: 执行自定义代码,处理复杂逻辑,支持 JavaScript 和 Python。

**配置项**:

```yaml
编程语言: JavaScript / Python
输入参数: 定义代码需要接收的变量
代码内容: 自定义代码逻辑
输出变量: 代码返回的结果
```

**JavaScript 示例**:

```javascript
// 输入: user_message (文本)
// 输出: order_id, products, request_time

function main({ user_message }) {
  // 从消息中提取订单号 (正则匹配)
  const orderMatch = user_message.match(/订单号?[：:]\s*(\d+)/);
  const order_id = orderMatch ? orderMatch[1] : null;
  
  // 提取商品名称 (关键词提取)
  const products = [];
  const productKeywords = ['手机', '电脑', '耳机', '平板', '充电器'];
  productKeywords.forEach(p => {
    if (user_message.includes(p)) products.push(p);
  });
  
  // 生成时间戳
  const timestamp = new Date().toISOString();
  
  return {
    order_id: order_id || "未知",
    products: products,
    product_count: products.length,
    request_time: timestamp
  };
}
```

**Python 示例**:

```python
# 输入: user_message (文本)
# 输出: intent_keywords

import re
from datetime import datetime

def main(user_message):
    # 提取关键词
    keywords = []
    if "退款" in user_message:
        keywords.append("退款")
    if "投诉" in user_message:
        keywords.append("投诉")
    
    # 生成时间戳
    timestamp = datetime.now().isoformat()
    
    return {
        "keywords": keywords,
        "timestamp": timestamp
    }
```

**关键点**:
- 适合做格式转换、数据清洗、正则提取等复杂逻辑
- 输入输出通过函数参数和 return 值传递
- 避免在代码节点中做网络请求 (用 HTTP 节点替代)
- 代码执行有超时限制,注意性能
- 可以引入部分标准库,但可能有安全限制

---

### 9. JSON 序列化节点 (JSON Serialize Node)

**作用**: 将对象或数组转换为 JSON 字符串,用于发送给外部接口。

**配置项**:

```yaml
输入对象: 对象或数组结构
输出变量: JSON字符串变量名
```

**使用示例**:

```yaml
JSON序列化节点配置:
  输入对象:
    case_id: "{{case_id}}"
    order_id: "{{order_id}}"
    intent: "{{intent}}"
    solution: "{{solution}}"
    products: "{{products}}"
    created_at: "{{request_time}}"
    
  输出变量: case_json_string
```

**输出结果**:

```json
{
  "case_id": "CS202603311234",
  "order_id": "12345",
  "intent": "退款申请",
  "solution": "已提交退款",
  "products": ["手机"],
  "created_at": "2026-03-31T10:30:00Z"
}
```

**关键点**:
- 将结构化数据转换为字符串,便于传输
- 常用于 HTTP 请求前的数据准备
- 可以自定义 JSON 格式

---

### 10. JSON 反序列化节点 (JSON Deserialize Node)

**作用**: 将 JSON 字符串解析为可访问字段的对象,与序列化节点相反。

**配置项**:

```yaml
输入: JSON字符串变量
输出对象字段定义:
  - 字段名: 变量名
    字段类型: 数据类型
```

**使用示例**:

```yaml
JSON反序列化节点配置:
  输入: "{{http_response}}"  # HTTP返回的JSON字符串
  
  输出对象字段定义:
    - 字段名: order_status
      类型: String
      说明: 订单状态
      
    - 字段名: product_name
      类型: String
      说明: 商品名称
      
    - 字段名: price
      类型: Number
      说明: 商品价格
      
    - 字段名: user_phone
      类型: String
      说明: 用户手机号
```

**输出变量**:
- 可以直接用 `{{order_status}}`、`{{product_name}}` 等访问字段

**关键点**:
- 常用于解析 HTTP 请求的响应
- 字段定义要准确,类型要匹配
- 解析失败可能导致工作流中断

---

### 11. 文本处理节点 (Text Processing Node)

**作用**: 对文本进行处理操作,如截取、替换、格式化、拼接等。

**支持的操作类型**:

| 操作类型 | 说明 | 示例 |
|---------|------|------|
| 文本拼接 | 将多个文本拼接成一个 | `"您好," + name + "!"` |
| 文本替换 | 替换指定内容 | `text.replace("旧词", "新词")` |
| 文本截取 | 截取子字符串 | `text.substring(0, 100)` |
| 格式化 | 按模板格式化 | `"订单号:{order_id}, 状态:{status}"` |
| 大小写转换 | 转换大小写 | `text.toUpperCase()` |
| 去除空白 | 去除首尾空格 | `text.trim()` |

**使用示例**:

```yaml
文本处理节点配置:
  操作类型: 文本拼接
  
  模板: |
    {{llm_reply}}
    
    ——————————————
    工单编号: {{case_id}}
    受理时间: {{request_time}}
    预计处理: 1-3个工作日
    如有疑问请拨打: 400-xxx-xxxx
    
  输出变量: final_reply
```

**关键点**:
- 可以组合多个操作
- 支持模板语法
- 适合简单的文本处理,复杂处理建议用代码节点

---

### 12. HTTP 请求节点 (HTTP Request Node)

**作用**: 调用外部 API 或 Web 服务,获取实时数据。

**配置项**:

```yaml
请求方式: GET / POST / PUT / DELETE
URL: 接口地址 (支持变量引用)
请求头: Headers 配置
请求体: Body 配置 (POST/PUT)
超时时间: 请求超时设置
```

**使用示例 - GET 请求**:

```yaml
HTTP请求节点配置:
  请求方式: GET
  URL: "https://api.myshop.com/orders/{{order_id}}"
  
  请求头:
    - Authorization: "Bearer {{api_token}}"
    - Content-Type: "application/json"
    
  超时: 10秒
  
  输出变量:
    - status_code: HTTP状态码
    - response_body: 响应体内容 (JSON字符串)
```

**使用示例 - POST 请求**:

```yaml
HTTP请求节点配置:
  请求方式: POST
  URL: "https://sms.api.com/send"
  
  请求头:
    - Authorization: "Bearer {{sms_token}}"
    - Content-Type: "application/json"
    
  请求体:
    phone: "{{user_phone}}"
    message: "您的售后申请{{case_id}}已受理"
    
  输出变量:
    - status_code: HTTP状态码
    - response_body: 响应体内容
```

**输出变量**:
- `status_code`: HTTP 状态码 (200、404、500 等)
- `response_body`: 响应体内容 (通常是 JSON 字符串)
- `response_headers`: 响应头信息

**关键点**:
- URL 和请求体支持变量引用
- 注意设置合理的超时时间
- 错误处理很重要,网络异常可能导致工作流中断
- 敏感信息 (如 API Token) 建议使用环境变量

---

## AI能力节点

### 13. 大模型节点 (LLM Node)

**作用**: 调用 AI 大模型进行文本生成、理解、推理,是最核心的节点之一。

**配置项**:

```yaml
模型选择: DeepSeek-V3 / GPT-4o / Doubao / Qwen 等
系统提示词 (System Prompt): 定义模型角色和行为边界
用户消息 (User Message): 具体任务描述
参数设置:
  - 温度 (Temperature): 控制创造性
  - 最大输出长度: Token 数限制
  - 是否流式输出: 实时返回或一次性返回
历史对话: 多轮对话上下文
绑定工具: 可调用的工具列表
```

**参数详解**:

| 参数 | 取值范围 | 说明 |
|------|---------|------|
| 温度 (Temperature) | 0.0 - 2.0 | 越低越稳定,越高越有创意。一般 0.5-0.8 |
| 最大输出长度 | 1 - 4096+ | 输出的最大 Token 数 |
| Top P | 0.0 - 1.0 | 核采样参数,影响多样性 |
| 频率惩罚 | 0.0 - 2.0 | 降低重复内容的概率 |
| 存在惩罚 | 0.0 - 2.0 | 鼓励谈论新话题 |

**使用示例**:

```yaml
大模型节点配置:
  模型: DeepSeek-V3
  
  系统提示词: |
    你是一个专业友好的售后客服,请根据用户的申请和订单信息,
    生成一段安抚用户情绪并说明处理方案的回复。
    语气要诚恳、简洁,不超过150字。
    
  用户消息: |
    用户申请: {{user_message}}
    意图类型: {{intent}}
    订单信息: {{order_info}}
    处理方案: {{solution}}
    
  参数设置:
    温度: 0.7
    最大输出长度: 500 tokens
    流式输出: 否
    
  输出变量:
    - llm_reply: 大模型生成的回复文本
```

**关键点**:
- Prompt 中用 `{{变量名}}` 引用上游节点的输出
- 系统提示词决定模型的"角色"和"行为边界"
- 温度越低输出越稳定,越高越有创意
- 可以绑定工具,让模型调用外部功能
- 历史对话字段用于实现多轮对话

---

### 14. 意图识别节点 (Intent Recognition Node)

**作用**: 自动判断用户输入属于哪种意图类型,无需手动编写规则。

**配置项**:

```yaml
输入: 待识别的文本
意图分类列表:
  - 意图名称: 分类标签
    描述: 触发条件描述
    示例: 典型触发句式
置信度阈值: 最低匹配度
默认意图: 未达到阈值时的默认分类
```

**使用示例**:

```yaml
意图识别节点配置:
  输入: "{{user_message}}"
  
  意图分类定义:
    - 名称: 售前_商品信息确认
      描述: 用户在询问商品的规格、材质、尺寸、功能、保质期、是否有货等
      示例:
        - "这个手机支持5G吗"
        - "衣服有M码吗"
        - "这个适合老人用吗"
        
    - 名称: 售前_优惠活动确认
      描述: 用户在询问优惠券、满减、会员折扣、大促规则、保价政策等
      示例:
        - "有优惠券吗"
        - "双十一打几折"
        - "买贵了能补差价吗"
        
    - 名称: 售中_订单查询
      描述: 用户在查询订单状态、支付状态、订单是否存在异常等
      示例:
        - "我的订单到哪一步了"
        - "支付成功了吗"
        
    - 名称: 售后_退换货服务
      描述: 用户在申请退货、换货,包含质量问题、发错货、破损等
      示例:
        - "我想退货"
        - "能换一个吗"
        - "收到的是坏的"
        
  置信度阈值: 0.6
  默认意图: 其他_闲聊
  
  输出变量:
    - intent: 识别出的意图名称
    - confidence: 置信度分数 (0~1)
    - primary_intent: 一级分类 (售前/售中/售后)
    - secondary_intent: 二级分类 (子类)
```

**输出变量**:
- `intent`: 完整意图标签 (如 "售前_商品信息确认")
- `confidence`: 置信度分数 (0.0~1.0)
- `primary_intent`: 一级分类 (可选)
- `secondary_intent`: 二级分类 (可选)

**关键点**:
- 意图描述要清晰、准确
- 提供足够多的示例句式
- 置信度阈值需要根据实际效果调整
- 未达到阈值时走默认意图

---

### 15. 问答节点 (Q&A Node)

**作用**: 基于知识库内容自动回答问题,结合 RAG (检索增强生成) 技术。

**配置项**:

```yaml
关联知识库: 知识库列表
用户问题: 待回答的问题
答案生成策略:
  - 优先使用知识库内容
  - 知识库无相关内容时: 使用大模型通用知识
  - 引用来源: 是否展示答案来源
提示词追加: 补充说明
```

**使用示例**:

```yaml
问答节点配置:
  关联知识库:
    - kb_presale_faq (售前FAQ库)
    - kb_product_manual (产品手册库)
    
  用户问题: "{{user_message}}"
  
  答案生成策略:
    优先使用知识库: 是
    知识库无内容时: 使用大模型通用知识
    引用来源: 展示
    
  提示词追加: |
    请只基于以上知识库内容回答,不要编造信息。
    如果知识库中没有相关内容,请明确告知用户。
    
  输出变量:
    - qa_answer: 生成的答案
    - qa_sources: 引用的知识来源列表
    - qa_confidence: 答案置信度
```

**输出变量**:
- `qa_answer`: 生成的答案文本
- `qa_sources`: 引用的知识来源列表
- `qa_confidence`: 答案置信度

**关键点**:
- 问答节点比大模型节点更专注于"找答案"
- 适合有明确知识库来源的场景
- 可以设置相似度阈值,过滤低质量答案
- 引用来源可以增加答案的可信度

---

## 知识库节点

### 16. 知识库检索节点 (Knowledge Base Search Node)

**作用**: 在知识库中进行语义搜索,找到最相关的内容。

**配置项**:

```yaml
目标知识库: 知识库名称
搜索查询: 查询文本
检索参数:
  - 返回数量 (Top K): 返回结果数
  - 相似度算法: cosine / dot_product
  - 最低相似度阈值: 过滤低质量结果
  - 过滤条件: 元数据筛选
```

**使用示例**:

```yaml
知识库检索节点配置:
  目标知识库: kb_faq
  
  搜索查询: "{{user_message}}"
  
  检索参数:
    top_k: 3
    相似度算法: cosine
    最低相似度: 0.75
    过滤条件:
      - category == "售前"
      
  高级配置:
    启用缓存: 是
    标题权重: 0.3
    内容权重: 0.7
    
  输出变量:
    - kb_results: 匹配的文档列表 (数组)
    - kb_results_count: 结果数量
    - kb_top_content: 第一条结果的内容
    - kb_similarity: 最高相似度分数
```

**输出变量**:
- `kb_results`: 匹配的文档数组,每项包含:
  - `content`: 文档内容
  - `title`: 文档标题
  - `score`: 相似度分数
  - `metadata`: 元数据
- `kb_results_count`: 结果数量
- `kb_top_content`: 第一条结果的内容
- `kb_similarity`: 最高相似度分数

**关键点**:
- 相似度阈值需要根据业务调整
- Top K 不宜过大,影响性能
- 可以通过元数据过滤缩小搜索范围
- 启用缓存可以提高重复查询的响应速度

---

### 17. 知识库写入节点 (Knowledge Base Write Node)

**作用**: 将文本内容写入知识库,供后续检索使用。

**配置项**:

```yaml
目标知识库: 知识库名称
写入内容:
  标题: 文档标题
  正文: 文档正文
元数据: 附加信息
```

**使用示例**:

```yaml
知识库写入节点配置:
  目标知识库: kb_after_sales_cases
  
  写入内容:
    标题: "{{intent}} - {{product_name}} - {{request_time}}"
    正文: |
      问题描述: {{user_message}}
      处理方案: {{solution}}
      处理结果: 已解决
      
  元数据:
    intent_type: "{{intent}}"
    product: "{{product_name}}"
    resolved: true
    user_id: "{{user_id}}"
    created_at: "{{request_time}}"
    
  输出变量:
    - kb_doc_id: 写入文档的ID
    - write_status: 写入状态 (成功/失败)
```

**关键点**:
- 写入的内容应该结构化,便于后续检索
- 元数据可以用于过滤和分类
- 写入操作有频率限制
- 适合积累案例和知识

---

### 18. 知识库删除节点 (Knowledge Base Delete Node)

**作用**: 从知识库中删除指定文档。

**配置项**:

```yaml
目标知识库: 知识库名称
删除方式:
  - 按文档ID: 指定文档ID
  - 按条件批量删除: 元数据过滤条件
```

**使用示例**:

```yaml
知识库删除节点配置:
  目标知识库: kb_after_sales_cases
  
  删除方式: 按文档ID
  文档ID: "{{kb_doc_id}}"
  
  # 或批量删除
  # 删除方式: 按条件
  # 过滤条件:
  #   - created_at < 365天前
  #   - status == "expired"
  
  输出变量:
    - delete_status: 删除状态 (成功/失败)
    - delete_count: 删除的文档数
```

**关键点**:
- 删除操作不可逆,谨慎使用
- 批量删除前建议先查询确认
- 定期清理过期内容,保持知识库质量

---

### 19. 知识库更新节点 (Knowledge Base Update Node)

**作用**: 更新知识库中已有文档的内容或元数据。

**配置项**:

```yaml
目标知识库: 知识库名称
文档ID: 要更新的文档ID
更新字段:
  - 字段名: 新值
```

**使用示例**:

```yaml
知识库更新节点配置:
  目标知识库: kb_after_sales_cases
  文档ID: "{{kb_doc_id}}"
  
  更新字段:
    title: "{{new_title}}"
    content: "{{new_content}}"
    metadata.status: "updated"
    metadata.updated_at: "{{current_time}}"
    
  输出变量:
    - update_status: 更新状态
```

**关键点**:
- 只更新指定的字段,其他字段保持不变
- 可以更新元数据中的特定字段
- 更新后可能需要重建索引

---

## 数据库节点

### 20. 数据库定义节点 (Database Schema Node)

**作用**: 定义数据库表结构,是使用数据库节点的前提。

**配置项**:

```yaml
数据库名称: 数据库名
表名: 表名
字段定义:
  - 字段名: 字段名称
    类型: 数据类型
    约束: 主键/唯一/非空等
    说明: 字段用途
```

**使用示例**:

```yaml
数据库定义节点配置:
  数据库名称: AfterSalesDB
  表名: cases
  
  字段定义:
    - 字段名: id
      类型: String (文本)
      约束: 主键, 自动生成
      
    - 字段名: case_id
      类型: String
      约束: 唯一, 非空
      说明: 工单号
      
    - 字段名: user_id
      类型: String
      约束: 非空
      说明: 用户ID
      
    - 字段名: order_id
      类型: String
      说明: 订单号
      
    - 字段名: intent
      类型: String
      说明: 意图类型
      
    - 字段名: status
      类型: String
      说明: 处理状态
      
    - 字段名: solution
      类型: String
      说明: 处理方案
      
    - 字段名: created_at
      类型: DateTime (时间)
      说明: 创建时间
      
    - 字段名: updated_at
      类型: DateTime
      说明: 更新时间
```

**关键点**:
- 字段类型要选择正确
- 主键和唯一约束要合理设置
- 建议添加 created_at 和 updated_at 字段

---

### 21. 数据库查询节点 (Database Query Node)

**作用**: 从数据库中查询数据 (SELECT)。

**配置项**:

```yaml
数据库: 数据库名
表名: 表名
查询条件: WHERE 条件
排序: ORDER BY 字段
返回数量: LIMIT 数量
```

**使用示例**:

```yaml
数据库查询节点配置:
  数据库: AfterSalesDB
  表名: cases
  
  查询条件:
    - user_id == {{user_id}}
    - created_at >= 最近30天
    - status != "deleted"
    
  排序: created_at DESC
  
  返回数量: 5
  
  输出变量:
    - query_results: 查询结果数组
    - result_count: 结果数量
```

**输出变量**:
- `query_results`: 查询结果数组
- `result_count`: 结果数量

**关键点**:
- 查询条件支持多个条件的 AND/OR 组合
- 可以使用变量引用
- 注意查询性能,避免全表扫描

---

### 22. 数据库新增节点 (Database Insert Node)

**作用**: 向数据库插入新记录 (INSERT)。

**配置项**:

```yaml
数据库: 数据库名
表名: 表名
插入数据:
  - 字段名: 值
```

**使用示例**:

```yaml
数据库新增节点配置:
  数据库: AfterSalesDB
  表名: cases
  
  插入数据:
    case_id: "{{case_id}}"
    user_id: "{{user_id}}"
    order_id: "{{order_id}}"
    intent: "{{intent}}"
    status: "processing"
    solution: "{{solution}}"
    created_at: "{{request_time}}"
    
  输出变量:
    - insert_result: 插入结果 (成功/失败)
    - inserted_id: 插入记录的ID
```

**输出变量**:
- `insert_result`: 插入结果 (成功/失败)
- `inserted_id`: 插入记录的ID

**关键点**:
- 必填字段不能为空
- 插入前可以检查唯一约束
- 建议使用事务保证数据一致性

---

### 23. 数据库更新节点 (Database Update Node)

**作用**: 修改数据库中已有记录 (UPDATE)。

**配置项**:

```yaml
数据库: 数据库名
表名: 表名
更新条件: WHERE 条件
更新字段:
  - 字段名: 新值
```

**使用示例**:

```yaml
数据库更新节点配置:
  数据库: AfterSalesDB
  表名: cases
  
  更新条件:
    - case_id == {{case_id}}
    
  更新字段:
    status: "resolved"
    updated_at: "{{current_time}}"
    
  输出变量:
    - update_count: 更新的记录数量
    - update_result: 更新结果
```

**输出变量**:
- `update_count`: 更新的记录数量
- `update_result`: 更新结果

**关键点**:
- 更新条件要精确,避免误更新
- 建议同时更新 updated_at 字段
- 可以批量更新多条记录

---

### 24. 数据库删除节点 (Database Delete Node)

**作用**: 删除数据库中的记录 (DELETE)。

**配置项**:

```yaml
数据库: 数据库名
表名: 表名
删除条件: WHERE 条件
确认提示: 安全确认
```

**使用示例**:

```yaml
数据库删除节点配置:
  数据库: AfterSalesDB
  表名: cases
  
  删除条件:
    - created_at < 180天前
    - status == "resolved"
    
  确认提示: 是
  
  输出变量:
    - delete_count: 删除的记录数
    - delete_result: 删除结果
```

**输出变量**:
- `delete_count`: 删除的记录数
- `delete_result`: 删除结果

**关键点**:
- 删除操作不可逆,谨慎使用
- 建议先用查询节点确认要删除的记录
- 可以考虑软删除 (设置 deleted 标志)

---

## 会话管理节点

### 25. 创建会话节点 (Session Create Node)

**作用**: 创建一个新的对话会话,为用户分配 session_id。

**配置项**:

```yaml
会话元数据: 会话相关信息
会话有效期: 过期时间设置
```

**使用示例**:

```yaml
创建会话节点配置:
  会话元数据:
    user_id: "{{user_id}}"
    channel: "{{channel}}"
    intent: "{{intent}}"
    created_at: "{{request_time}}"
    
  会话有效期: 7天
  
  输出变量:
    - session_id: 新创建的会话ID
    - session_info: 完整会话信息对象
```

**输出变量**:
- `session_id`: 新创建的会话ID
- `session_info`: 完整会话信息对象

**关键点**:
- 会话用于管理多轮对话
- 可以设置会话有效期
- 元数据用于记录会话相关信息

---

### 26. 查询会话节点 (Session Query Node)

**作用**: 根据条件查询已有会话信息。

**配置项**:

```yaml
查询条件: WHERE 条件
排序: ORDER BY 字段
返回数量: LIMIT 数量
```

**使用示例**:

```yaml
查询会话节点配置:
  查询条件:
    - user_id == {{user_id}}
    - status == "active"
    
  排序: created_at DESC
  
  返回数量: 1
  
  输出变量:
    - existing_session: 查询到的会话对象 (没有则为null)
    - has_active_session: 是否有进行中的会话 (true/false)
```

**输出变量**:
- `existing_session`: 查询到的会话对象
- `has_active_session`: 是否有进行中的会话

**关键点**:
- 用于判断用户是否有进行中的会话
- 可以实现会话续接功能

---

### 27. 更新会话节点 (Session Update Node)

**作用**: 更新会话的状态或元数据。

**配置项**:

```yaml
会话ID: 要更新的会话ID
更新字段:
  - 字段名: 新值
```

**使用示例**:

```yaml
更新会话节点配置:
  会话ID: "{{session_id}}"
  
  更新字段:
    last_active_at: "{{current_time}}"
    status: "active"
    metadata.last_intent: "{{intent}}"
    
  输出变量:
    - update_status: 更新状态
```

---

### 28. 查询会话历史节点 (Get Conversation History Node)

**作用**: 获取指定会话中的历史消息列表,用于大模型理解上下文。

**配置项**:

```yaml
会话ID: 会话标识
获取数量: 最近N条消息
消息类型: 全部/仅用户/仅AI
排序: 时间顺序
```

**使用示例**:

```yaml
查询会话历史节点配置:
  会话ID: "{{session_id}}"
  获取数量: 6  # 最近3轮对话 (user+assistant各3条)
  消息类型: 全部
  排序: 时间倒序
  
  输出变量:
    - history_messages: 消息历史数组
    - history_count: 消息总数
    - is_new_session: 是否为新会话
```

**输出变量**:
- `history_messages`: 消息数组,格式:
  ```json
  [
    {"role": "user", "content": "...", "time": "..."},
    {"role": "assistant", "content": "...", "time": "..."}
  ]
  ```
- `history_count`: 总消息数
- `is_new_session`: 是否为新会话

**关键点**:
- 用于实现多轮对话
- 建议限制获取条数,避免 token 超限
- 可以过滤特定类型的消息

---

## 消息管理节点

### 29. 创建消息节点 (Message Create Node)

**作用**: 在指定会话中创建 (保存) 一条新消息。

**配置项**:

```yaml
会话ID: 所属会话
消息角色: user / assistant / system
消息内容: 消息文本
元数据: 附加信息
```

**使用示例**:

```yaml
# 保存用户消息
创建消息节点配置:
  会话ID: "{{session_id}}"
  角色: user
  内容: "{{user_message}}"
  元数据:
    intent: "{{intent}}"
    confidence: "{{confidence}}"
    channel: "{{channel}}"
    timestamp: "{{request_time}}"
    
  输出变量:
    - user_msg_id: 用户消息ID

---
# 保存AI回复
创建消息节点配置:
  会话ID: "{{session_id}}"
  角色: assistant
  内容: "{{final_reply}}"
  元数据:
    sub_intent: "{{secondary_intent}}"
    case_id: "{{case_id}}"
    model_used: "DeepSeek-V3"
    timestamp: "{{current_time}}"
    
  输出变量:
    - assistant_msg_id: AI消息ID
```

**输出变量**:
- `message_id`: 消息的唯一ID

**关键点**:
- 每轮对话应该保存两条消息 (用户消息 + AI回复)
- 元数据用于记录消息相关信息
- 消息保存是实现多轮对话的基础

---

### 30. 查询消息节点 (Message Query Node)

**作用**: 查询指定会话或条件下的消息记录。

**配置项**:

```yaml
查询条件: WHERE 条件
排序: ORDER BY 字段
返回数量: LIMIT 数量
```

**使用示例**:

```yaml
查询消息节点配置:
  查询条件:
    - session_id == {{session_id}}
    # 或 user_id == {{user_id}}
    - role == "user"  # 可选: 只查用户消息
    - created_at >= 最近30天
    
  排序: created_at DESC
  
  返回数量: 20
  
  输出变量:
    - messages: 消息列表数组
    - total_count: 总消息数量
```

**输出变量**:
- `messages`: 消息数组
- `total_count`: 总消息数量

---

### 31. 修改消息节点 (Message Update Node)

**作用**: 修改已保存的消息内容或元数据。

**配置项**:

```yaml
消息ID: 要修改的消息ID
修改字段:
  - 字段名: 新值
```

**使用示例**:

```yaml
修改消息节点配置:
  消息ID: "{{message_id}}"
  
  修改字段:
    metadata.status: "resolved"
    metadata.case_id: "{{case_id}}"
    metadata.resolved_at: "{{current_time}}"
    
  输出变量:
    - update_success: 是否更新成功
```

---

### 32. 删除消息节点 (Message Delete Node)

**作用**: 删除指定的消息记录。

**配置项**:

```yaml
删除方式:
  - 按消息ID: 指定消息ID
  - 按会话ID: 删除该会话的所有消息
```

**使用示例**:

```yaml
删除消息节点配置:
  删除方式: 按消息ID
  消息ID: "{{message_id}}"
  
  # 或批量删除
  # 删除方式: 按会话ID
  # 会话ID: "{{session_id}}"
  
  输出变量:
    - delete_success: 是否删除成功
    - delete_count: 删除的消息数
```

---

## 异步处理节点

### 33. 异步任务节点 (Async Task Node)

**作用**: 在不阻塞主流程的情况下,在后台执行耗时操作。

**配置项**:

```yaml
任务内容: 子流程节点列表
触发时机: 何时触发
等待结果: 是否等待完成
超时时间: 任务超时设置
```

**使用示例**:

```yaml
异步任务节点配置:
  触发时机: 主流程输出节点执行完毕后
  
  等待结果: 否  # fire and forget
  
  超时时间: 30秒
  
  任务内容 (子流程):
    1. 数据库写入节点:
       - 保存工单记录
       
    2. HTTP请求节点:
       - 调用短信接口发通知
       - URL: "https://sms.api.com/send"
       - Body: {phone: "{{user_phone}}", message: "您的售后申请已受理"}
       
    3. 知识库写入节点:
       - 记录本次案例
       - 标题: "{{intent}} - {{timestamp}}"
       
  输出变量:
    - async_task_id: 异步任务ID
    - async_status: 任务状态 (启动/完成/失败)
```

**关键点**:
- 主流程不需要等待异步任务完成
- 适合发通知、写日志等不影响用户等待的操作
- 异步任务内部的错误不会导致主流程失败
- 注意设置合理的超时时间

---

## 节点组合最佳实践

### 常见节点组合模式

#### 1. FAQ 优先问答模式

```
输入节点
  ↓
知识库检索节点 (FAQ库)
  ↓
条件分支节点 (相似度 >= 0.85?)
  ├─ 是 → 问答节点 → 输出节点
  └─ 否 → 意图识别节点 → 业务分支处理 → 输出节点
```

#### 2. 多轮对话模式

```
输入节点 (session_id)
  ↓
查询会话历史节点
  ↓
大模型节点 (带历史对话)
  ↓
创建消息节点 (保存对话)
  ↓
输出节点
```

#### 3. 数据查询处理模式

```
输入节点
  ↓
代码节点 (提取关键词)
  ↓
HTTP请求节点 (查询API)
  ↓
JSON反序列化节点
  ↓
条件分支节点 (数据状态)
  ↓
大模型节点 (生成回复)
  ↓
输出节点
```

#### 4. 批量并行处理模式

```
输入节点
  ↓
数据库查询节点 (获取列表)
  ↓
批处理节点 (并行处理)
  ↓
变量聚合节点
  ↓
输出节点
```

#### 5. 异步后台任务模式

```
主流程:
  输入节点 → 业务处理 → 大模型节点 → 输出节点
                                         ↓
                                    异步任务节点
                                         ↓
                         ┌───────────────┼───────────────┐
                         ↓               ↓               ↓
                    数据库写入      知识库写入      HTTP通知
```

---

### 节点选择指南

| 需求场景 | 推荐节点组合 |
|---------|------------|
| **简单问答** | 输入 → 知识库检索 → 问答 → 输出 |
| **意图分流** | 输入 → 意图识别 → 条件分支 → 多分支处理 → 输出 |
| **数据处理** | 输入 → 代码节点 → 数据库操作 → 输出 |
| **外部API集成** | 输入 → HTTP请求 → JSON反序列化 → 处理 → 输出 |
| **多轮对话** | 输入 → 查询历史 → 大模型(带历史) → 创建消息 → 输出 |
| **批量操作** | 输入 → 数据库查询 → 循环/批处理 → 聚合 → 输出 |
| **后台任务** | 主流程 → 异步任务 (写库/通知) |

---

## 性能优化建议

### 1. 减少不必要的节点
- 合并相似逻辑
- 使用代码节点处理复杂逻辑,替代多个简单节点

### 2. 合理使用异步节点
- 将不影响用户体验的操作放异步
- 写日志、发通知等操作异步执行

### 3. 知识库优化
- 设置合理的相似度阈值
- 控制 Top K 数量
- 使用元数据过滤缩小搜索范围

### 4. 大模型节点优化
- 选择合适的模型 (简单任务用小模型)
- 控制输出长度
- 合理设置温度参数

### 5. 数据库优化
- 添加索引
- 避免全表扫描
- 限制查询数量

---

## 调试技巧

### 1. 使用输出节点查看中间结果
在关键节点后添加临时输出节点,查看变量值。

### 2. 条件分支添加日志
在每个分支添加变量赋值节点,记录分支执行情况。

### 3. 捕获异常
使用条件分支节点判断上游节点是否成功执行。

### 4. 分步测试
先测试单个节点,再逐步连接整个流程。

---

## 总结

Coze 平台提供了丰富的节点类型,涵盖:

- **基础功能**: 输入输出
- **流程控制**: 条件分支、循环、批处理
- **数据处理**: 代码、变量操作、JSON处理
- **AI 能力**: 大模型、意图识别、问答
- **知识管理**: 知识库增删改查
- **数据持久化**: 数据库操作
- **对话管理**: 会话和消息管理
- **异步处理**: 后台任务

合理组合这些节点,可以构建出功能强大的智能应用。建议:

1. **从简单开始**: 先搭建基础流程,再逐步增加功能
2. **理解节点本质**: 每个节点都有特定的用途和适用场景
3. **注重性能**: 避免过度复杂的流程
4. **善用异步**: 不阻塞主流程的操作尽量异步执行
5. **持续优化**: 根据实际使用效果调整节点配置

---

*文档版本: v1.0 | 更新时间: 2026年3月31日*
