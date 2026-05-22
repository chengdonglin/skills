# Strategy Pattern Design Specification

## Purpose

策略模式用于封装一组可互换业务算法，并在运行时动态选择执行策略。

适用于：

- 支付方式切换
- 登录方式切换
- 通知渠道切换
- 文件解析策略
- AI模型切换
- 风控规则切换
- 价格计算切换
- 数据导出方式切换

不适用于：

- 固定流程骨架（应使用模板模式）
- 顺序执行节点（应使用责任链）
- 复杂分叉路由（应使用规则树）

---

# Core Design Rule

策略模式必须：

- 每种算法独立实现
- 通过 Factory 动态获取
- 策略之间完全解耦
- 调用方不出现条件分支

禁止：

```java
if(type.equals("A")){
   ...
}else if(type.equals("B")){
   ...
}
```

禁止：

```java
switch(type)
```

进行策略分发。

必须通过策略工厂获取。

---

# Standard Project Structure

必须生成：

```text
application/
   strategy/
      factory/
      interface/
      impl/
```

禁止：

```text
utils/
common/
helper/
```

策略属于业务行为，不属于工具类。

---

# Strategy Interface Naming Rule

必须：

```text
XxxStrategy
```

允许：

- PaymentStrategy
- LoginStrategy
- ExportStrategy
- RiskCheckStrategy
- AiModelStrategy

禁止：

- IHandler
- Processor
- ServiceImpl
- StrategyService

---

# Concrete Strategy Naming Rule

必须：

```text
BusinessName + Strategy
```

允许：

- AlipayStrategy
- WechatPayStrategy
- PasswordLoginStrategy
- SmsLoginStrategy
- CsvExportStrategy
- PdfExportStrategy

禁止：

- StrategyImpl
- DemoStrategy
- Strategy1

必须语义化。

---

# Strategy Contract Rule

必须定义：

```java
R execute(T request);
```

允许扩展：

```java
boolean supports(String type);
```

禁止：

```java
process()
handle()
run()
```

统一使用：

```java
execute
```

---

# Strategy Selection Rule

必须通过：

```java
StrategyFactory
```

选择策略。

例如：

```java
factory.get(type).execute(req);
```

禁止：

```java
if(type)
switch(type)
```

---

# Factory Naming Rule

必须：

```text
XxxStrategyFactory
```

允许：

- PaymentStrategyFactory
- LoginStrategyFactory
- ExportStrategyFactory

禁止：

- StrategyManager
- StrategyHolder
- StrategyContainer

---

# Factory Registration Rule

必须使用 Spring 自动注入：

```java
@Resource
private List<XxxStrategy> strategies;
```

初始化：

```java
@PostConstruct
```

注册：

```java
Map<String,XxxStrategy>
```

禁止手动：

```java
new AlipayStrategy()
```

禁止硬编码：

```java
map.put("ALI",...)
```

应由策略自身声明支持类型。

---

# Strategy Self Identification Rule

每个策略必须声明：

```java
String type();
```

例如：

```java
@Override
public String type(){
    return "ALIPAY";
}
```

禁止工厂写死：

```java
if(strategy instanceof ...)
```

---

# Dependency Injection Rule

策略允许注入：

- DomainService
- Repository
- RPC Client
- MQ Producer

例如：

```java
@Resource
private PaymentDomainService domainService;
```

禁止：

策略互相注入：

```java
@Resource
private OtherStrategy strategy;
```

策略必须完全解耦。

---

# Business Responsibility Rule

每个策略只负责一种算法。

禁止：

一个策略同时：

- 支付
- 校验
- MQ通知
- 状态同步

必须拆分。

---

# Application Layer Restriction

默认生成到：

```text
application.strategy
```

禁止默认生成：

```text
domain
infrastructure
```

除非用户明确指定领域策略。

---

# Exception Rule

允许：

```java
throw new BusinessException(...)
```

禁止吞异常：

```java
catch(Exception e){}
```

禁止返回 null 表示失败。

---

# Anti Patterns

禁止生成：

## if-else派发

```java
if(type.equals(...))
```

---

## switch派发

```java
switch(type)
```

---

## 工厂硬编码注册

```java
map.put(...)
```

---

## 策略互调

```java
otherStrategy.execute()
```

---

## 巨型策略

一个类实现多个业务算法。

---

# Output Requirement

生成代码必须：

- Java 21
- Spring Boot 3+
- Lombok
- Spring自动注册
- Factory动态获取
- execute统一入口
- 可直接运行
- 无 TODO
- 无伪代码

---

# Final Mandatory Rule

生成策略模式代码必须包含：

1. Strategy Interface
2. Concrete Strategies
3. StrategyFactory
4. Spring 自动注册
5. 调用示例
6. 测试代码

不得生成：

- if/else分发
- switch分发
- 手写new注册
- 硬编码策略绑定