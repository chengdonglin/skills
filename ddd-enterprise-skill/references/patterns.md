# Design Pattern Selection Rules

根据业务自动选择设计模式。

---

# Strategy Pattern

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

# Factory Pattern

用于：

- Aggregate creation
- Adapter creation
- Policy creation

生成：

```java
XXXFactory
```

禁止：

```java
new XXX()
```

---

# Chain of Responsibility

触发条件：

- 生命周期阶段
- 校验流水线
- 多阶段处理

生成：

```java
XXXProcessChain
```

必须支持自动注册。

---

# Specification Pattern

复杂业务校验。

生成：

```java
XXXSpecification
```

禁止：

```java
if (...) throw ...
```

---

# Template Method

流程固定、步骤扩展时生成。

生成：

```java
AbstractXXXProcessor
```

---

# Registry Pattern

需要插件化扩展时生成：

```java
XXXRegistry
```

例如：

- Strategy registry
- Handler registry
- Processor registry

必须支持 Spring 自动装配。

---

# Adapter Pattern

用于：

- Redis
- MQ
- RPC
- Third-party service

生成：

```java
XXXAdapter
```

禁止直接调用 SDK。

---

# State Modeling

如果存在状态流转：

生成：

```java
XXXStatus
```

并封装行为：

```java
activate()
complete()
cancel()
```

禁止：

```java
setStatus()
```

---

# Event Driven Pattern

状态变化必须触发事件。

例如：

```java
Created
Activated
Completed
Failed
```

应用层统一发布。

---

# Pattern Priority

优先级：

1. Rich Domain
2. Specification
3. Factory
4. Strategy
5. Chain
6. Template
7. Adapter

必须优先保证领域表达能力。