```markdown
# Design Diagrams

## Integrated Architecture Diagram

```mermaid
graph TD
    A[Frontend 'React']
    B[API Routes (Flask) <br/>(HTTPS in production)]
    C[Service Layer]
    D[Repository Layer]
    E[MongoDB]
    F[Shared Utilities]

    A -->|HTTP/HTTPS Requests| B
    B --> C
    C --> D
    D --> E
    C --- F
    B --- F
```

## Data Flow Diagram

```mermaid
graph LR
    Client[Client Request <br/>'HTTPS in production']
    Routes[API Routes (Flask)]
    Services[Business Logic]
    Repos[Data Access Layer]
    DB[MongoDB]

    Client --> Routes
    Routes --> Services
    Services --> Repos
    Repos --> DB
    DB --> Repos
    Repos --> Services
    Services --> Routes
    Routes --> Client
```

## Component Interaction Diagram

```mermaid
graph TD
    subgraph "Frontend"
        FE[React App]
    end

    subgraph "Backend"
        AR[API Routes]
        SL[Service Layer]
        RL[Repository Layer]
        DB[MongoDB]
    end

    FE -->|HTTP/HTTPS| AR
    AR --> SL
    SL --> RL
    RL --> DB
    SL ---|Uses| "Shared Utilities (Logger, Config)"
    AR --- "Shared Utilities (Logger, Config)"
```
