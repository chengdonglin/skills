---

name: enterprise-ddd-generator
description: Generate enterprise-grade multi-module Java DDD code from live MySQL schema and business requirements.
version: 1.0.0
author: linchengdong
license: MIT


---

# Enterprise DDD Generator

Generate enterprise-grade Spring Boot 3 + MyBatis Plus DDD code using:

- live database schema
- business requirement
- request parameters
- design pattern references

---

# Inputs

Required:

## database

MySQL database name

Example:

```text
aigc_prod
```

---

## request

Request object name

Example:

```text
ActivateDeviceRequest
```

---

## requirement

Business requirement

Example:

```text
实现设备激活模块，支持幂等、状态校验、生命周期管理
```

---

# Tools

This skill uses:

## Python Script Execution

Execute:

```bash
python scripts/load_schema.py <database>
```

Produces:

```json
schema.json
```

Used as source of truth.

---

# Runtime Workflow

## Step 1 — Inspect Schema

Run:

```bash
python scripts/load_schema.py <database>
```

Read:

- tables
- columns
- pk
- fk
- indexes
- comments

Generate:

```json
schema.json
```

Never invent schema.

---

## Step 2 — Infer DDD Model

Infer:

- aggregate root
- child entities
- value objects
- repository boundary
- domain service
- domain events

Must prefer rich domain behavior.

Correct:

```java
device.activate()
```

Wrong:

```java
device.setStatus()
```

---

## Step 3 — Load References

Must load:

```text
references/ddd-rules.md
references/naming.md
references/chain-rule.md
references/template-pattern-design.md
references/strategy-pattern-design.md
```

These override default generation behavior.

---

## Step 4 — Load Assets

Use:

```text
assets/aggregate.java
assets/repository.java
assets/factory.java
assets/strategy.java
assets/chain.java
assets/specification.java
```

Generated code must match style.

---

## Step 5 — Select Patterns

Automatically choose:

### Chain

Sequential workflow

Reference:

```text
reference/chain-rule.md
```

---

### Template

Stable lifecycle workflow

Reference:

```text
reference/template-pattern-design.md
```

---

### Strategy

Behavior switching by type

Reference:

```text
reference/strategy-pattern-design.md
```

---

### Specification

Complex domain rule validation

---

### Factory

Always generate aggregate factory

Forbidden:

```java
new Aggregate()
```

inside application layer.

---

## Step 6 — Generate Project

Must generate:

```text
project-parent
 ├── project-interfaces
 ├── project-application
 ├── project-domain
 ├── project-infrastructure
 └── project-shared
```

Never flat CRUD structure.

Forbidden:

```text
controller
service
mapper
entity
```

---

# Layer Rules

## interfaces

Generate:

- Controller
- Request DTO
- Response DTO
- Assembler

No business logic.

---

## application

Generate:

- ApplicationService
- UseCase orchestration
- transaction boundary
- event publish
- pattern assembly

No persistence details.

---

## domain

Generate:

- AggregateRoot
- Entity
- ValueObject
- DomainService
- Repository interface
- DomainEvent
- Specification
- Factory

Must be pure domain.

No infrastructure dependency.

---

## infrastructure

Generate:

- PO
- Mapper
- RepositoryImpl
- Convertor

No business decision logic.

---

## shared

Generate:

- Result
- Exception
- Constants
- BaseEnum

No business logic.

---

# Output Contract

Must output in order:

## 1 Schema Analysis

Explain:

- tables
- fk
- aggregate reasoning

---

## 2 DDD Modeling Decision

Explain:

- aggregate split
- selected patterns

---

## 3 Project Tree

```text
...
```

---

## 4 Complete Code Files

Requirements:

- directly runnable
- no TODO
- no pseudo code
- production grade

---

# Quality Standard

Generated code must reflect:

- high cohesion
- low coupling
- OCP
- plugin extensibility
- maintainability

Never generate tutorial/demo code.