# PES1UG24AM385_SELAB1 — Community Solar Credit Allocation Manager

## Lab 1: Requirements Engineering & UML Use-Case Modelling

**Problem Statement:** #63  
**Domain:** Sustainability & Green Tech  
**Student:** Pradeep  
**SRN:** PES1UG24AM385  

---

## Project Overview

The **Community Solar Credit Allocation Manager** is a clean-energy sharing portal that manages rooftop solar generation, surplus solar credits, peer-to-peer credit transfers, and monthly utility billing offsets within a neighborhood microgrid.

### Actors

- **Smart Meter** – Provides solar generation data.
- **Prosumer Resident** – Manages and transfers solar credits.
- **Co-op Manager** – Monitors community solar and billing records.

### Key Use Cases

- Record Solar Generation
- Calculate Surplus Credits
- Transfer Solar Credits
- View Credit Balance
- Apply Billing Offset
- Generate Monthly Statement
- View Community Records
- Authenticate User

### UML Relationships

- `UC-01 → UC-02` — `<<include>>`
- `UC-03 → UC-05` — `<<include>>`
- `UC-06 → UC-07` — `<<extend>>`

---

## Core Use Case

**UC-03 — Transfer Solar Credits**

The prosumer can transfer available solar credits to another participating resident. The system validates the credit balance, performs the transfer, updates both accounts, and records the transaction.

**Alternate Flow:** If the requested transfer exceeds the available balance, the system rejects the transfer and displays an insufficient-balance message.

---

### Tools

- PlantUML
- draw.io
- GitHub
