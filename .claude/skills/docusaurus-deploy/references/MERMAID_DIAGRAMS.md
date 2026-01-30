# Mermaid Diagram Reference

This reference covers Mermaid diagram syntax and usage in Docusaurus.

## Setup

### Installation

```bash
npm install @docusaurus/theme-mermaid
```

### Configuration

```typescript
// docusaurus.config.ts
themes: [
  [
    require.resolve('@docusaurus/theme-mermaid'),
    {
      theme: {
        light: 'default',
        dark: 'dark',
      },
    },
  ],
];

markdown: {
  mermaid: true,
};
```

## Diagram Types

### Flowchart

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

**Directions:**
- `TD` / `TB` - Top to Bottom
- `LR` - Left to Right
- `RL` - Right to Left

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB

    User->>API: Request
    API->>DB: Query
    DB-->>API: Result
    API-->>User: Response
```

### Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +eat()
        +sleep()
    }
    class Dog {
        +bark()
    }
    Animal <|-- Dog
```

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing
    Processing --> Success
    Processing --> Error
    Success --> [*]
    Error --> Idle
```

### Entity Relationship

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
```

### User Journey

```mermaid
journey
    title User Journey
    section Signup
      Visit site: 5: Me
      Sign up: 3: Me
      Verify email: 2: Me
    section Onboarding
      Welcome email: 5: Me
      First project: 4: Me
```

### Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Design
    Research: 2025-01-01, 5d
    Wireframes: 2025-01-06, 3d
    section Development
    Backend: 2025-01-09, 10d
    Frontend: 2025-01-15, 7d
```

### Pie Chart

```mermaid
pie title Distribution
    "Python" : 40
    "JavaScript" : 30
    "TypeScript" : 20
    "Other" : 10
```

### Mindmap

```mermaid
mindmap
  root((Project))
    Frontend
      React
      Next.js
    Backend
      FastAPI
      PostgreSQL
    Infrastructure
      Docker
      Kubernetes
```

## Styling

### Themes

```mermaid
%%{init: {'theme':'base', 'themeVariables': {
  'primaryColor':'#ffcccc',
  'edgeLabelBackground':'#ffffff'
}}}%%
graph TD
    A[Node A] --> B[Node B]
```

### Custom Classes

```mermaid
graph TD
    A[Node A]:::class1
    B[Node B]:::class2
    A --> B

    classDef class1 fill:#f9f,stroke:#333
    classDef class2 fill:#bbf,stroke:#333
```

## Syntax Reference

### Nodes

```
[Square]
(Rounded)
[(Stadium)]
{Cylinder}
[/Parallelogram/]
[[Subroutine]]
[(Database)]
[/Trapezoid\]
```

### Connections

```
-->    Arrow
---    Line
-.->   Dotted
===>   Thick
```

### Text

```
Node[Label]           # Center label
Node[Line\nBreak]     # Multi-line
Node["Special <chars>"]  # Escape special chars
```

## Best Practices

1. **Keep it simple** - Complex diagrams are hard to read
2. **Use consistent styling** - Same colors for similar elements
3. **Add titles** - Describe what the diagram shows
4. **Test in editor** - Use mermaid.live to preview
5. **Limit size** - Large diagrams may break on mobile

## Troubleshooting

**Problem:** Diagram not rendering

**Solutions:**
- Verify `@docusaurus/theme-mermaid` is installed
- Check `markdown.mermaid: true` in config
- Look for syntax errors in diagram code

**Problem:** Diagram overflow

**Solutions:**
- Simplify complex diagrams
- Break into multiple diagrams
- Use CSS to control overflow
