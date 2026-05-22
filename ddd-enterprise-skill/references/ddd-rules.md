# DDD Rules

必须严格遵守领域驱动设计。

---

# Rich Domain Model

领域对象必须拥有行为。

正确：

```java
device.activate();
device.offline();
device.heartbeat();
```

错误：

```java
device.setStatus();
device.setOnline(true);
```

禁止贫血模型。

---

# Aggregate Root Rule

聚合根负责：

- 一致性边界
- 生命周期控制
- 子实体协调

一个事务只能修改一个聚合根。

禁止跨聚合直接修改。

---

# Entity Rule

Entity 必须具备：

- identity
- business behavior
- 生命周期

禁止纯 getter/setter 数据结构。

---

# Value Object Rule

ValueObject 必须：

- immutable
- equals/hashCode
- 无独立 identity

例如：

```java
DeviceNumber
UploadStatus
Money
Address
```

---

# Repository Rule

Repository 只定义：

```java
save()
findById()
remove()
exists()
```

复杂查询禁止放 Repository。

查询型逻辑应在基础设施层实现。

---

# Domain Service Rule

仅在：

多个聚合协作

时允许生成。

禁止把所有业务塞进 DomainService。

---

# Factory Rule

聚合必须通过工厂创建。

正确：

```java
DeviceFactory.create()
```

错误：

```java
new Device()
```

---

# Domain Event Rule

状态变化必须记录事件。

例如：

```java
DeviceActivatedEvent
UploadCompletedEvent
```

领域内部：

```java
domainEvents.add(...)
```

应用层统一发布。

---

# Application Service Rule

ApplicationService 负责：

- 编排
- 事务
- 协调

禁止：

- SQL
- Mapper
- 领域规则判断

---

# Infrastructure Rule

只负责：

- Persistence
- MQ
- Redis
- RPC
- Adapter

禁止业务逻辑。

---

# Dependency Rule

允许：

interfaces -> application  
application -> domain  
infrastructure -> domain  
all -> shared

禁止：

domain -> infrastructure  
domain -> application  
application -> interfaces

必须严格检查。