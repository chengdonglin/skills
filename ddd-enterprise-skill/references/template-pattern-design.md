# Template Pattern Design Specification

## Purpose

模板模式用于定义业务执行骨架，将稳定流程固化在父类中，把可变逻辑下沉到子类实现。

适用于：

- 订单处理流程
- 审批执行流程
- 文件导入导出流程
- AI任务执行流程
- 支付流程
- 同步任务流程
- 消息消费流程
- 状态转换流程

不适用于：

- 多分支动态路由（应使用责任链）
- 节点动态组合（应使用责任链）
- 策略动态切换（应使用策略模式）

---

# Core Design Rule

模板模式必须：

- 父类定义标准流程
- 子类只实现差异步骤
- 执行顺序固定
- 子类不得修改主流程顺序

禁止：

```java
if (...) {
   stepA();
} else {
   stepB();
}
```

在模板主流程中做业务分支。

模板负责流程骨架，不负责业务决策。

---

# Standard Project Structure

必须生成：

```text
application/
   template/
      abstracts/
         AbstractXxxTemplate.java
      impl/
         XxxTemplate.java
```

禁止：

```text
service/template
utils/template
common/template
```

模板属于业务流程设计，应放 application。

---

# Abstract Template Naming Rule

必须：

```text
Abstract + BusinessName + Template
```

允许：

- AbstractOrderSubmitTemplate
- AbstractRefundTemplate
- AbstractImportTemplate
- AbstractAiTaskTemplate

禁止：

- BaseTemplate
- TemplateService
- TemplateHandler
- CommonTemplate

命名必须语义化。

---

# Concrete Template Naming Rule

必须：

```text
BusinessName + Template
```

允许：

- OrderSubmitTemplate
- RefundApproveTemplate
- AiTaskExecuteTemplate

禁止：

- TemplateImpl
- Template1
- DemoTemplate

---

# Template Method Rule

模板主方法必须：

```java
public final R execute(T request)
```

必须 final。

禁止子类覆盖。

禁止：

```java
public R process()
```

非 final。

---

# Standard Execution Flow

模板主流程必须按顺序：

## 1. validate

参数校验

```java
validate(request);
```

---

## 2. beforeExecute

前置准备

```java
beforeExecute(request);
```

---

## 3. doExecute

核心业务

```java
R result = doExecute(request);
```

---

## 4. afterExecute

后置处理

```java
afterExecute(request,result);
```

---

## 5. onSuccess

成功回调

```java
onSuccess(request,result);
```

---

## 6. onException

异常补偿

```java
onException(request,e);
```

---

禁止调整执行顺序。

---

# Required Abstract Methods

子类必须实现：

```java
protected abstract void validate(T request);

protected abstract R doExecute(T request);
```

---

# Optional Hook Methods

允许覆写：

```java
protected void beforeExecute(T request)

protected void afterExecute(T request,R result)

protected void onSuccess(T request,R result)

protected void onException(T request,Exception e)
```

默认空实现。

禁止强制所有子类实现。

---

# Exception Rule

模板父类统一捕获：

```java
catch (Exception e)
```

统一：

```java
onException(...)
throw e;
```

禁止子类吞异常：

```java
catch(Exception e){}
```

---

# Dependency Injection Rule

模板子类允许：

```java
@Resource
private XxxDomainService domainService;
```

允许：

- DomainService
- Repository
- RPC Client
- MQ Producer

禁止：

注入其他模板：

```java
@Resource
private OtherTemplate template;
```

模板之间不得互相调用。

---

# Business Responsibility Rule

模板只定义：

业务流程骨架

子类只负责：

具体业务实现

禁止：

父类写具体业务：

```java
saveOrder();
callPayment();
```

这些必须在子类。

---

# Application Layer Restriction

模板默认生成到：

```text
application.template
```

禁止默认生成到：

```text
domain
infrastructure
```

除非用户明确指定。

---

# Anti Patterns

禁止生成：

## 巨型模板类

```java
if...
else...
switch...
```

---

## 子类覆盖 execute

```java
@Override
execute()
```

---

## 模板互调

```java
otherTemplate.execute()
```

---

## 空模板骨架

```java
execute(){
   doExecute()
}
```

必须完整生命周期。

---

# Output Requirement

生成代码必须：

- Java 21
- Spring Boot 3+
- Lombok
- final execute
- Hook完整
- 可直接运行
- 无 TODO
- 无伪代码
- 命名语义化

---

# Final Mandatory Rule

生成模板模式代码时必须包含：

1. AbstractTemplate
2. ConcreteTemplate
3. execute模板流程
4. Hook方法
5. 示例调用代码
6. Spring Bean注入方式

不得省略生命周期设计。