# Naming Convention

必须统一。

---

# Aggregate Root

正确：

```java
Device
Order
UploadTask
UserAccount
```

禁止：

```java
DeviceEntity
DeviceModel
DeviceBean
```

---

# Repository

正确：

```java
DeviceRepository
OrderRepository
```

禁止：

```java
DeviceDao
DeviceMapperService
```

---

# Factory

正确：

```java
DeviceFactory
OrderFactory
```

禁止：

```java
DeviceBuilderUtil
```

---

# Specification

正确：

```java
DeviceActivateSpecification
OrderPaySpecification
```

禁止：

```java
DeviceCheckUtil
```

---

# Strategy

正确：

```java
DeviceRegisterStrategy
UploadPolicyStrategy
```

禁止：

```java
DeviceTypeHandler
```

---

# Registry

正确：

```java
DeviceStrategyRegistry
ProcessorRegistry
```

---

# Chain

正确：

```java
UploadProcessChain
DeviceInitChain
```

禁止：

```java
UploadExecutor
```

---

# Domain Event

正确：

```java
DeviceCreatedEvent
OrderPaidEvent
UploadCompletedEvent
```

禁止：

```java
DeviceEvent
OrderMsg
```

---

# Application Service

正确：

```java
DeviceApplicationService
OrderApplicationService
```

禁止：

```java
DeviceManager
DeviceServiceImpl
```

---

# Infrastructure Impl

正确：

```java
DeviceRepositoryImpl
```

禁止：

```java
DeviceDaoImpl
```

---

# Persistence Object

正确：

```java
DevicePO
OrderPO
```

禁止：

```java
DeviceDO
DeviceEntity
```

---

# Assembler

正确：

```java
DeviceAssembler
OrderAssembler
```

禁止：

```java
DeviceConverterUtil
```

---

# Shared Classes

正确：

```java
BaseException
Result
DomainException
```

禁止：

```java
CommonUtil
BaseHelper
GlobalManager
```

---

# Forbidden Naming

禁止生成：

```java
Util
Helper
Manager
BaseBusiness
CommonService
GenericHandler
MiscProcessor
```

---

# Method Naming

行为驱动：

正确：

```java
activate()
complete()
heartbeat()
register()
cancel()
```

禁止：

```java
setStatus()
updateFlag()
processData()
handle()
doSomething()
```

必须具备明确业务语义。