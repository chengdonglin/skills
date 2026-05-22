---
name: enterprise-ddd-generator
description: Generate enterprise-grade multi-module Java DDD code from business requirements and live database schema. Automatically inspect database structure using scripts, infer aggregates, choose proper design patterns, and generate extensible Spring Boot + MyBatis Plus implementations.
---

# Enterprise DDD Generator

根据：

- 用户业务需求
- 数据库名称
- 当前数据库实时表结构

自动生成：

- 企业级多模块 DDD 工程
- Spring Boot 3
- MyBatis Plus
- 可运行
- 可扩展
- Rich Domain Model
- 优雅设计模式驱动

---

# Activation Conditions

当用户提供：

- 开发需求
- 数据库名称

例如：

```text
数据库：aigc_prod

需求：

实现设备激活模块
支持：
- 激活
- 状态校验
- 幂等
```

必须激活 Skill。

---

# Required Workflow

必须严格执行。

---

# Step 1：读取数据库结构

执行：

```bash
python scripts/load_schema.py <database_name>
```

读取：

- tables
- columns
- indexes
- foreign keys
- constraints

生成：

```json
schema.json
```

禁止臆造字段。

必须严格依据真实 schema。

---

# Step 2：分析业务需求

提取：

- 生命周期行为
- 状态流转
- 核心业务动作
- 校验规则
- 聚合边界候选

例如：

```text
设备激活
```

推导：

```java
device.activate()
```

禁止：

```java
device.setStatus()
```

---

# Step 3：推导领域模型

识别：

## Aggregate Root

例如：

```java
Device
Order
UploadTask
```

---

## Child Entity

存在生命周期依附对象时生成。

---

## Value Object

例如：

```java
DeviceNumber
UploadStatus
```

---

## Repository Interface

定义领域仓储。

---

## Domain Service

仅在跨聚合业务时生成。

---

# Step 4：自动推导设计模式


---

## Strategy Pattern

触发条件：

存在：

- type
- mode
- protocol
- route

生成：

```java
XXXStrategy
XXXStrategyRegistry
```

禁止：

```java
if(type == ...)
```

---

## Factory Pattern

必须生成：

```java
XXXFactory
```

用于聚合创建。

禁止直接：

```java
new Aggregate()
```

---

## Chain of Responsibility

触发条件：

- 多阶段流程
- 生命周期流水线
- 校验管道

生成：

```java
XXXProcessChain
```

必须支持自动注册扩展。

---

## Specification Pattern

复杂校验规则：

```java
XXXSpecification
```

禁止：

```java
if (...) throw ...
```

---

## Template Method

流程骨架稳定时生成：

```java
AbstractXXXProcessor
```

---

## Domain Event

状态变化生成：

```java
XXXCreatedEvent
XXXActivatedEvent
XXXCompletedEvent
```

领域内部记录：

```java
domainEvents.add(...)
```

应用层统一发布。

---

# Step 5：加载资源规范

读取：

- references/ddd-rules.md
- references/patterns.md
- references/naming.md

确保统一架构。

---

# Step 6：参考代码模板

参考：

- assets/aggregate.java
- assets/repository.java
- assets/factory.java
- assets/strategy.java
- assets/chain.java
- assets/specification.java

统一生成风格。

---

# Step 7：生成多模块工程

必须生成：

```text
${project-name}-parent
 ├── ${project-name}-interfaces
 ├── ${project-name}-application
 ├── ${project-name}-domain
 ├── ${project-name}-infrastructure
 └── ${project-name}-shared
```

禁止单 module。

禁止：

```text
controller
service
mapper
entity
```

混杂结构。

---

# Module Responsibilities

## interfaces

职责：

- Controller
- Request DTO
- Response DTO
- Assembler
- 参数校验
- HTTP 协议适配

依赖：

```text
application
shared
```

禁止：

- Repository
- Mapper
- Domain规则

控制器必须极薄：

```java
assembler.toCommand(request)
applicationService.execute()
```

---

## application

职责：

业务用例编排。

包含：

- ApplicationService
- Transaction Boundary
- 聚合协调
- Event Publish

依赖：

```text
domain
shared
```

禁止：

- SQL
- Mapper
- 持久化细节

原则：

一个 public method = 一个业务能力

例如：

```java
activate()
register()
heartbeat()
```

---

## domain

职责：

核心业务。

包含：

- AggregateRoot
- Entity
- ValueObject
- Factory
- Specification
- DomainEvent
- Repository Interface
- DomainService

依赖：

```text
shared
```

禁止依赖：

```text
application
interfaces
infrastructure
```

必须 Rich Domain：

正确：

```java
device.activate()
```

错误：

```java
device.setStatus()
```

---

## infrastructure

职责：

技术实现。

包含：

- RepositoryImpl
- Mapper
- PO
- Redis Adapter
- MQ Adapter
- RPC Adapter

依赖：

```text
domain
shared
```

禁止业务规则。

---

## shared

职责：

基础能力共享。

包含：

- Result
- BaseException
- Constants
- BaseEnum

禁止业务逻辑。

---

# Dependency Rules (Strict)

允许：

```text
interfaces -> application
application -> domain
infrastructure -> domain
all -> shared
```

禁止：

```text
domain -> infrastructure
domain -> application
application -> interfaces
```

违反时必须修正。

---

# MyBatis Plus Rules

PO：

```java
DevicePO
```

Mapper：

```java
DeviceMapper
```

RepositoryImpl：

负责：

PO <-> Domain 转换

不得包含业务规则。

字段必须与数据库一致。

禁止新增不存在字段。

---

# Naming Rules

允许：

```java
DeviceFactory
DeviceRepository
DeviceAssembler
DeviceActivateSpecification
DeviceProcessChain
DeviceStrategyRegistry
```

禁止：

```java
DeviceUtil
CommonService
Helper
Manager
BaseBusiness
```

---

# Output Order (Mandatory)

必须严格按以下顺序输出。

---

## 1. Schema 分析

说明：

- 使用了哪些表
- 字段作用
- 外键关系
- 聚合边界依据

---

## 2. DDD 建模说明

解释：

- 为什么这样划分聚合
- 为什么选择这些设计模式

---

## 3. 模块职责说明

解释：

- interfaces
- application
- domain
- infrastructure
- shared

各自作用。

---

## 4. Maven 多模块目录结构

输出：

```text
tree structure
```

---

## 5. 完整代码文件

格式：

```java
// 职责：设备聚合根
public class Device
```

代码必须：

- 可直接运行
- 风格统一
- 可扩展
- 企业级优雅

---

# Ambiguous Rules

如果需求不完整：

优先依据：

1. 数据库结构
2. 表关系
3. references 规范
4. assets 模板

自动补全最佳实践。

禁止退化成 CRUD。

---

# Quality Standard

生成代码必须像：

大型企业资深架构师编写。

必须具备：

- 高内聚
- 低耦合
- 开闭原则
- 自动扩展能力
- 插件化设计
- 工程可维护性

绝不生成教学式 Demo。