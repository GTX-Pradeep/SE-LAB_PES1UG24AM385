# SELAB3 — Component Modelling & Architectural Pattern Selection

## Lab Overview

This lab focuses on component modelling, architectural style selection, UML component diagrams, interfaces, and component dependencies.

### Scenario

**Self-Service Coffee Kiosk System**

The kiosk supports:

- Coffee selection: Espresso, Americano, Latte
- Drink sizes: Small and Large
- Credit-card payment
- Receipt printing
- Touchscreen interaction
- Menu and pricing storage

## Architecture Selected

**Layered Architecture**

The architecture was selected because it provides clear separation of concerns and is suitable for the focused functionality of the self-service kiosk.

### Key Components

1. Touchscreen UI
2. Order Manager
3. Payment Service
4. Menu & Pricing Database
5. Receipt Printer

### Interfaces

1. Order Management API
2. Payment Processing
3. Menu/Pricing Query
4. Receipt Printing

## Deliverables

| File | Description |
|---|---|
| `Lab_3_Component_Diagram.pdf` | UML component diagram |
| `SELAB3_Architecture_Justification.pdf` | Architecture selection, justification, security and performance discussion |

## Architecture Highlights

- **Separation of concerns:** Each component has a focused responsibility.
- **Security:** Payment processing is isolated in the Payment Service.
- **Performance:** Dedicated components keep ordering and other operations separated.

---

**Course Lab:** Software Engineering Lab (SELAB)  
**Lab:** 3 — Component Modelling & Architectural Pattern Selection
