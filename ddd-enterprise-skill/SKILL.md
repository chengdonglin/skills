---
name: enterprise-ddd-generator
description: Generate enterprise-grade multi-module Java DDD code from live database schema and business requirements. Automatically inspect MySQL schema using scripts, infer aggregates, apply design-pattern references, and generate extensible Spring Boot 3 + MyBatis Plus code.
---

# Enterprise DDD Generator

Generate production-grade multi-module DDD code from:

- database name
- business requirement
- request parameters
- live database schema inspection

Output must be:

- runnable
- extensible
- rich domain model
- enterprise-grade architecture

---

# Activation Conditions

Activate when user provides:

- database name
- business requirement

Example:

```text
数据库：aigc_prod

请求：ActivateDeviceRequest

需求：

实现设备激活模块

支持：

- 激活
- 幂等
- 状态校验
- 生命周期管理
```

Immediately execute generation workflow.

Never ask for table schema manually.

---

# Required Runtime Workflow

Must execute strictly.

---

# Step 1 — Execute Schema Inspection Script

Execute:

```bash
python scripts/load_schema.py <database_name>
```

This script queries live MySQL:

- tables
- columns
- primary keys
- indexes
- foreign keys
- comments

Produces:

```json
schema.json
```

Must use generated schema only.

Forbidden:

- hallucinated fields
- invented table relation
- fake foreign key

Schema is source of truth.

---

# Step 2 — Parse Business Requirement

Extract:

- business lifecycle
- state transitions
- domain actions
- constraints
- aggregate candidates
- workflow characteristics

Example:

```text
设备激活
```

Infer:

```java
device.activate()
```

Forbidden:

```java
device.setStatus()
```

Must prefer rich domain behavior.

---

# Step 3 — Infer DDD Model

Generate:

## Aggregate Root

Examples:

- Device
- LeaveOrder
- UploadTask

---

## Child Entity

Only if lifecycle depends on aggregate root.

---

## Value Object

Examples:

- DeviceNo
- ActivateStatus
- LeaveReason

---

## Repository Interface

Domain abstraction only.

---

## Domain Service

Generate only for cross-aggregate coordination.

---

## Domain Events

When lifecycle mutation exists:

```java
DeviceActivatedEvent
LeaveSubmittedEvent
TaskCompletedEvent
```

Domain records internally:

```java
domainEvents.add(...)
```

Application publishes.

---

# Step 4 — Auto Select Design Patterns

Pattern selection must follow references strictly.

---

## Responsibility Chain

Trigger when:

- sequential validation
- approval pipeline
- process interception
- staged lifecycle processing

Must load:

```text
reference/chain-rule.md
```

Generate only:

- business handlers
- DynamicContext extension
- RuleFactory
- LinkArmory assembly

Default layer:

```text
application.chain
```

Never regenerate framework internals.

---

## Template Pattern

Trigger when:

- stable lifecycle workflow
- fixed process skeleton

Load:

```text
reference/template-pattern-design.md
```

Generate:

- AbstractTemplate
- ConcreteTemplate
- final execute lifecycle

Default layer:

```text
application.template
```

---

## Strategy Pattern

Trigger when requirement includes:

- type
- mode
- protocol
- route
- channel

Load:

```text
reference/strategy-pattern-design.md
```

Generate:

- Strategy interface
- concrete strategies
- StrategyFactory

Default layer:

```text
application.strategy
```

Forbidden:

```java
if(type==...)
switch(type)
```

---

## Factory Pattern

Always generate aggregate factory:

```java
XxxFactory
```

Forbidden:

```java
new Aggregate()
```

directly in application layer.

---

## Specification Pattern

Generate for complex domain validation:

```java
XxxSpecification
```

Forbidden:

```java
if (...) throw ...
```

inside aggregate root.

---

Patterns may coexist.

Prefer enterprise-best composition.

Examples:

- Template + Chain
- Template + Strategy
- Chain + Strategy

---

# Step 5 — Load References

Must load and obey:

```text
reference/ddd-rules.md
reference/naming.md
reference/chain-rule.md
reference/template-pattern-design.md
reference/strategy-pattern-design.md
```

These override default generation behavior.

---

# Step 6 — Load Assets

Use code style from:

```text
assets/aggregate.java
assets/repository.java
assets/factory.java
assets/strategy.java
assets/chain.java
assets/specification.java
```

Generated code must match asset style.

---

# Step 7 — Generate Multi-Module Project

Must generate:

```text
${project-name}-parent
 ├── ${project-name}-interfaces
 ├── ${project-name}-application
 ├── ${project-name}-domain
 ├── ${project-name}-infrastructure
 └── ${project-name}-shared
```

Forbidden:

```text
controller
service
mapper
entity
```

flat CRUD project.

---

# Module Responsibility Rules

## interfaces

Generate:

- Controller
- Request DTO
- Response DTO
- Assembler

Only protocol adaptation.

Forbidden:

- repository access
- domain mutation logic

Controller must remain thin:

```java
assembler.toCommand(request)
applicationService.execute()
```

---

## application

Generate:

- ApplicationService
- transaction boundary
- use-case orchestration
- event publish
- pattern orchestration

Forbidden:

- SQL
- Mapper
- persistence detail

One public method = one use case.

Examples:

```java
submit()
activate()
heartbeat()
approve()
```

---

## domain

Generate:

- AggregateRoot
- Entity
- ValueObject
- Factory
- Specification
- DomainEvent
- Repository interface
- DomainService

Forbidden dependencies:

- application
- interfaces
- infrastructure

Must be rich domain model.

Correct:

```java
device.activate()
```

Wrong:

```java
device.setStatus()
```

---

## infrastructure

Generate:

- RepositoryImpl
- Mapper
- PO
- Convertor
- Redis Adapter
- MQ Adapter
- RPC Adapter

Forbidden:

business decision logic.

---

## shared

Generate:

- Result
- BaseException
- Constants
- BaseEnum

No business logic.

---

# Dependency Rules (Strict)

Allowed:

```text
interfaces -> application
application -> domain
infrastructure -> domain
all -> shared
```

Forbidden:

```text
domain -> infrastructure
domain -> application
application -> interfaces
```

Must auto-correct violations.

---

# Persistence Rules

Generate:

## PO

```java
DevicePO
```

---

## Mapper

```java
DeviceMapper
```

MyBatis-Plus style.

---

## RepositoryImpl

Responsible only for:

PO ↔ Domain conversion

No business logic.

Field definitions must match live schema exactly.

Never invent columns.

---

# Naming Rules

Allowed:

- DeviceFactory
- LeaveApprovalChainFactory
- PasswordLoginStrategy
- AbstractLeaveSubmitTemplate
- DeviceActivateSpecification

Forbidden:

- Util
- Manager
- Helper
- CommonService
- Logic101
- DemoHandler

Names must be semantic.

---

# Output Order (Mandatory)

Must output strictly in this order.

---

## 1. Schema Analysis

Explain:

- tables used
- column meaning
- foreign keys
- aggregate boundary reasoning

---

## 2. DDD Modeling Decision

Explain:

- aggregate split
- chosen patterns
- domain reasoning

---

## 3. Module Responsibility

Explain:

- interfaces
- application
- domain
- infrastructure
- shared

---

## 4. Maven Multi-Module Tree

Output full project structure.

---

## 5. Complete Code Files

Code must be:

- directly runnable
- unified style
- production-grade
- extensible

No pseudo code.

No TODO.

---

# Ambiguity Resolution

If requirement is incomplete:

Infer using priority:

1. live schema
2. foreign keys
3. references
4. assets
5. enterprise DDD best practice

Never degrade into CRUD scaffolding.

---

# Quality Standard

Generated code must look like written by:

senior enterprise platform architect

Must demonstrate:

- high cohesion
- low coupling
- open/closed principle
- extensibility
- plugin architecture
- maintainability

Never generate tutorial/demo code.