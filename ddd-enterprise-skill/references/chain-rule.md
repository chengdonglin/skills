# Responsibility Chain Application Coding Specification

## Purpose

本规范约束 Application 层责任链业务实现方式。

责任链基础设施已经存在于框架中，业务代码只能继承或实现已有抽象。

禁止重新生成以下基础设施：

- ILink
- LinkedList
- DynamicContext
- ILogicHandler
- BusinessLinkedList
- LinkArmory

这些类属于框架层，由系统统一提供。

业务层只允许：

- 实现 ILogicHandler
- 扩展 DynamicContext
- 使用 LinkArmory 装配责任链
- 注入 BusinessLinkedList 执行业务链

## 抽象责任链的代码如下：

### 链接口

```

/**
 * @description 
 * @create 2025-01-18 09:27
 */
public interface ILink<E> {

    boolean add(E e);

    boolean addFirst(E e);

    boolean addLast(E e);

    boolean remove(Object o);

    E get(int index);

    void printLinkList();

}

```

### 功能链路

```

/**
 * @description 功能链路
 * @create 2025-01-18 09:31
 */
public class LinkedList<E> implements ILink<E> {

    /**
     * 责任链名称
     */
    private final String name;

    transient int size = 0;

    transient Node<E> first;

    transient Node<E> last;

    public LinkedList(String name) {
        this.name = name;
    }

    void linkFirst(E e) {
        final Node<E> f = first;
        final Node<E> newNode = new Node<>(null, e, f);
        first = newNode;
        if (f == null)
            last = newNode;
        else
            f.prev = newNode;
        size++;
    }

    void linkLast(E e) {
        final Node<E> l = last;
        final Node<E> newNode = new Node<>(l, e, null);
        last = newNode;
        if (l == null) {
            first = newNode;
        } else {
            l.next = newNode;
        }
        size++;
    }

    @Override
    public boolean add(E e) {
        linkLast(e);
        return true;
    }

    @Override
    public boolean addFirst(E e) {
        linkFirst(e);
        return true;
    }

    @Override
    public boolean addLast(E e) {
        linkLast(e);
        return true;
    }

    @Override
    public boolean remove(Object o) {
        if (o == null) {
            for (Node<E> x = first; x != null; x = x.next) {
                if (x.item == null) {
                    unlink(x);
                    return true;
                }
            }
        } else {
            for (Node<E> x = first; x != null; x = x.next) {
                if (o.equals(x.item)) {
                    unlink(x);
                    return true;
                }
            }
        }
        return false;
    }

    E unlink(Node<E> x) {
        final E element = x.item;
        final Node<E> next = x.next;
        final Node<E> prev = x.prev;

        if (prev == null) {
            first = next;
        } else {
            prev.next = next;
            x.prev = null;
        }

        if (next == null) {
            last = prev;
        } else {
            next.prev = prev;
            x.next = null;
        }

        x.item = null;
        size--;
        return element;
    }

    @Override
    public E get(int index) {
        return node(index).item;
    }

    Node<E> node(int index) {
        if (index < (size >> 1)) {
            Node<E> x = first;
            for (int i = 0; i < index; i++)
                x = x.next;
            return x;
        } else {
            Node<E> x = last;
            for (int i = size - 1; i > index; i--)
                x = x.prev;
            return x;
        }
    }

    public void printLinkList() {
        if (this.size == 0) {
            System.out.println("链表为空");
        } else {
            Node<E> temp = first;
            System.out.print("目前的列表，头节点：" + first.item + " 尾节点：" + last.item + " 整体：");
            while (temp != null) {
                System.out.print(temp.item + "，");
                temp = temp.next;
            }
            System.out.println();
        }
    }

    protected static class Node<E> {

        E item;
        Node<E> next;
        Node<E> prev;

        public Node(Node<E> prev, E element, Node<E> next) {
            this.item = element;
            this.next = next;
            this.prev = prev;
        }

    }

    public String getName() {
        return name;
    }

}

```

### 流程流转控制

```



/**
 * @author Fuzhengwei bugstack.cn @小傅哥
 * @description 业务链路
 * @create 2025-01-18 10:27
 */
public class BusinessLinkedList<T, D extends DynamicContext, R> extends LinkedList<ILogicHandler<T, D, R>> implements ILogicHandler<T, D, R> {

    public BusinessLinkedList(String name) {
        super(name);
    }

    @Override
    public R apply(T requestParameter, D dynamicContext) throws Exception {
        Node<ILogicHandler<T, D, R>> current = this.first;
        do {
            ILogicHandler<T, D, R> item = current.item;
            try {
                // 1. 前置调用
                R applyBefore = item.applyBefore(requestParameter, dynamicContext);
                if (!dynamicContext.isProceed()) {
                    item.applyAfter(requestParameter, dynamicContext, applyBefore);
                    return applyBefore;
                }

                // 2. 节点跳过
                if (dynamicContext.isJump()) {
                    current = current.next;
                    continue;
                }

                // 3. 执行节点
                R apply = item.apply(requestParameter, dynamicContext);
                if (!dynamicContext.isProceed()) {
                    item.applyAfter(requestParameter, dynamicContext, apply);
                    return apply;
                }

                current = current.next;

            } catch (Exception e) {
                item.applyAfterException(requestParameter, dynamicContext, e);
                throw e;
            }

        } while (null != current);

        throw new RuntimeException("current item dynamic proceed is error");
    }

}


```

### 流程控制方法

```

/**
 * @description 逻辑处理器
 * @create 2025-01-18 09:43
 */
public interface ILogicHandler<T, D extends DynamicContext, R> {

    default R next(T requestParameter, D dynamicContext) {
        dynamicContext.setJump(false);
        dynamicContext.setProceed(true);
        return null;
    }

    default R stop(T requestParameter, D dynamicContext, R result) {
        dynamicContext.setJump(false);
        dynamicContext.setProceed(false);
        return result;
    }

    default R jump(T requestParameter, D dynamicContext, R result) {
        dynamicContext.setJump(true);
        dynamicContext.setProceed(true);
        return result;
    }

    R apply(T requestParameter, D dynamicContext) throws Exception;

    default R applyBefore(T requestParameter, D dynamicContext) throws Exception {
        dynamicContext.setJump(false);
        return null;
    }

    default void applyAfter(T requestParameter, D dynamicContext, R result) throws Exception {
    }

    default void applyAfterException(T requestParameter, D dynamicContext, Exception e) throws Exception {
    }

}


```

### 链路动态上下文

```

import java.util.HashMap;
import java.util.Map;

/**
 * 
 * 2025/7/12 16:34
 */
public class DynamicContext {

    /**
     * 节点放行标识
     */
    private boolean proceed;

    /**
     * 跳过当前节点
     */
    private boolean jump;

    public DynamicContext() {
        this.proceed = true;
        this.jump = false;
    }

    private final Map<String, Object> dataObjects = new HashMap<>();

    public <T> void setValue(String key, T value) {
        dataObjects.put(key, value);
    }

    public <T> T getValue(String key) {
        return (T) dataObjects.get(key);
    }

    public boolean isProceed() {
        return proceed;
    }

    public void setProceed(boolean proceed) {
        this.proceed = proceed;
    }

    public boolean isJump() {
        return jump;
    }

    public void setJump(boolean jump) {
        this.jump = jump;
    }

}


```

### 链路装配

```

/**
 * @description 链路装配
 * @create 2025-01-18 10:02
 */
public class LinkArmory<T, D extends DynamicContext, R> {

    private final BusinessLinkedList<T, D, R> logicLink;

    @SafeVarargs
    public LinkArmory(String linkName, ILogicHandler<T, D, R>... logicHandlers) {
        logicLink = new BusinessLinkedList<>(linkName);
        for (ILogicHandler<T, D, R> logicHandler: logicHandlers){
            logicLink.add(logicHandler);
        }
    }

    public BusinessLinkedList<T, D, R> getLogicLink() {
        return logicLink;
    }

}

```

## 责任链的使用方法如下：

```
@Slf4j
@Service
public class RuleLogic101 extends AbstractLogicLink<String, Rule02TradeRuleFactory.DynamicContext, String> {

    @Override
    public String apply(String requestParameter, Rule02TradeRuleFactory.DynamicContext dynamicContext) throws Exception {

        log.info("link model01 RuleLogic101");

        return next(requestParameter, dynamicContext);
    }

}

@Slf4j
@Service
public class RuleLogic102 extends AbstractLogicLink<String, Rule02TradeRuleFactory.DynamicContext, String> {

    @Override
    public String apply(String requestParameter, Rule02TradeRuleFactory.DynamicContext dynamicContext) throws Exception {

        log.info("link model01 RuleLogic102");

        return "link model01 单实例链";
    }

}

使用方式如下：

@Service
public class Rule02TradeRuleFactory {

    @Bean("demo01")
    public BusinessLinkedList<String, DynamicContext, XxxResponse> demo01(RuleLogic201 ruleLogic201,
                                                                          RuleLogic202 ruleLogic202,
                                                                          RuleLogic203 ruleLogic203) {

        LinkArmory<String, DynamicContext, XxxResponse> linkArmory = new LinkArmory<>("demo01", ruleLogic201, ruleLogic202, ruleLogic203);

        return linkArmory.getLogicLink();
    }

    @Bean("demo02")
    public BusinessLinkedList<String, DynamicContext, XxxResponse> demo02(RuleLogic202 ruleLogic202, RuleLogic203 ruleLogic203) {

        LinkArmory<String, DynamicContext, XxxResponse> linkArmory = new LinkArmory<>("demo02", ruleLogic202, ruleLogic203);

        return linkArmory.getLogicLink();
    }

    @EqualsAndHashCode(callSuper = true)
    @Data
    @Builder
    @AllArgsConstructor
    @NoArgsConstructor
    public static class DynamicContext extends cn.bugstack.wrench.design.framework.link.model2.DynamicContext {
        private String age;
    }

}


  @Resource(name = "demo01")
    private BusinessLinkedList<String, Rule02TradeRuleFactory.DynamicContext, XxxResponse> businessLinkedList01;

    @Resource(name = "demo02")
    private BusinessLinkedList<String, Rule02TradeRuleFactory.DynamicContext, XxxResponse> businessLinkedList02;

    @Test
    public void test_model02_01() throws Exception {
        XxxResponse apply = businessLinkedList01.apply("123", new Rule02TradeRuleFactory.DynamicContext());
        log.info("测试结果:{}", JSON.toJSONString(apply));
    }

    @Test
    public void test_model02_02() throws Exception {
        XxxResponse apply = businessLinkedList01.apply("123", new Rule02TradeRuleFactory.DynamicContext());
        log.info("测试结果:{}", JSON.toJSONString(apply));
    }

```



---

# Mandatory Inheritance Rule

业务节点必须：

```java
implements ILogicHandler<
    Request,
    XxxRuleFactory.DynamicContext,
    Response
>
```

或者继承业务统一抽象：

```java
extends AbstractXxxLogicHandler
```

（若业务工程存在）

禁止重新生成：

```java
public interface ILogicHandler
```

禁止复制框架实现。

---

# DynamicContext Extension Rule

业务上下文必须扩展框架 DynamicContext：

```java
@EqualsAndHashCode(callSuper = true)
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public static class DynamicContext
extends cn.xxx.link.DynamicContext {

    private String userId;

    private String orderId;

    private String traceId;

}
```

允许增加：

- userId
- orderId
- bizCode
- traceId
- riskScore
- custom state

禁止覆盖：

- proceed
- jump
- dataObjects

禁止重写：

- setProceed
- setJump
- getValue
- setValue

---

# Handler Naming Rule

必须语义化命名：

允许：

- OrderValidateHandler
- RiskCheckHandler
- InventoryLockHandler
- PaymentExecuteHandler
- RefundAuditHandler

禁止：

- RuleLogic101
- RuleLogic102
- demo01
- handler1
- logicA

示例命名仅作演示，禁止直接生成。

---

# Handler Lifecycle Rule

业务节点允许实现：

## applyBefore

适合：

- 参数校验
- 幂等校验
- 熔断
- 鉴权
- 条件预判

示例：

```java
@Override
public XxxResponse applyBefore(...) {
    if (...) {
        return stop(...);
    }
    return next(...);
}
```

---

## apply

核心业务逻辑：

```java
@Override
public XxxResponse apply(...)
```

适合：

- 查询
- 规则计算
- 调用领域服务
- 聚合协调

---

## applyAfter

适合：

- metrics
- trace
- audit
- cleanup

---

## applyAfterException

适合：

- rollback
- compensate
- alarm
- log

---

# Flow Control Rule

允许：

继续：

```java
return next(req,ctx);
```

终止：

```java
return stop(req,ctx,result);
```

跳过：

```java
return jump(req,ctx,result);
```

禁止：

```java
return null;
```

禁止：

```java
throw new RuntimeException("skip");
```

控制流程。

---

# Handler Dependency Rule

禁止节点互相注入：

```java
@Resource
private PaymentHandler paymentHandler;
```

禁止：

```java
paymentHandler.apply(...)
```

节点必须完全解耦。

节点之间共享数据必须通过：

```java
ctx.setValue(...)
ctx.getValue(...)
```

---

# Factory Rule

责任链工厂必须：

```java
@Service
public class XxxRuleFactory
```

链路必须通过：

```java
@Bean
```

暴露。

例如：

```java
@Bean("orderSubmitChain")
```

允许：

- orderSubmitChain
- refundAuditChain
- memberUpgradeChain

禁止：

- demo01
- demo02

---

# Link Assembly Rule

必须：

```java
new LinkArmory<>(
    "业务链名称",
    handlerA,
    handlerB,
    handlerC
)
```

禁止：

```java
setNext()
appendNext()
```

禁止动态拼接链指针。

---

# Invocation Rule

必须注入：

```java
@Resource(name = "业务链Bean")
private BusinessLinkedList<...> chain;
```

执行：

```java
chain.apply(req,new XxxRuleFactory.DynamicContext())
```

禁止直接调用节点：

```java
handler.apply(...)
```

---

# Exception Rule

业务异常必须正常抛出：

```java
throw e;
```

补偿逻辑统一放：

```java
applyAfterException(...)
```

禁止吞异常：

```java
catch(Exception e){}
```

---

# Business Coding Style

每个 Handler 只能负责一个职责。

禁止：

一个节点同时：

- 参数校验
- 查库存
- 扣库存
- 调支付
- 发MQ

正确拆分：

- ValidateHandler
- InventoryHandler
- PaymentHandler
- NotifyHandler

---

# Anti Patterns

禁止生成：

## 巨型业务链节点

```java
if...
else...
if...
```

---

## 节点互相调用

```java
otherHandler.apply()
```

---

## 重写框架基础设施

```java
public interface ILogicHandler
```

---

## 自定义链实现

```java
setNext()
```

---

## JDK LinkedList 替代

```java
new java.util.LinkedList()
```

---

# Output Requirement

生成代码必须：

- 基于已有责任链框架
- 只生成业务实现
- 不生成框架抽象
- Java 21
- Spring Boot 3+
- Lombok
- 可直接复制运行
- 无 TODO
- 无伪代码

---

# Final Mandatory Rule

生成业务责任链代码时：

只生成：

1. DynamicContext 扩展
2. 业务 Handler
3. RuleFactory
4. 链装配
5. 调用示例
6. 测试代码

绝不生成责任链底层框架实现。