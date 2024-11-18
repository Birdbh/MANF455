# MANF455
## A **Supercharged** MES for Your **MPS Drilling Station** 🚀🚀🚀

This document outlines the design of a **next-level** Manufacturing Execution System (MES) for your MPS Drilling Station. It's here to **revolutionize** your production process and help you make **smarter decisions** 🧠🧠🧠.

**Key Features:**

* **Real-time monitoring 👀👀👀:** Keep a **close eye** on your machine with live data.
* **Improved scheduling 🗓️🗓️🗓️:** Plan and optimize production schedules for **maximum efficiency**.
* **Enhanced decision-making 🧠🧠🧠:** Gain **valuable insights** from data to make **informed choices**.
* **Modular design 🧩🧩🧩:** Easily adapt the system to different stations with minimal changes. 

**User-Friendly Interface:**

* **Simple and intuitive UI 🧑‍💻🧑‍💻🧑‍💻:** Designed for all user types (operators, technicians, managers).
* **Operator window 👷‍♀️👷‍♀️👷‍♀️:** Submit work orders, monitor production status, and add new customers. 
* **Technician window 🔧🔧🔧:** View and manage downtime events (start/stop, reasons). 
* **Manager window 📊📊📊:** Generate reports, export data, and visualize Overall Equipment Effectiveness (OEE). 

**Under the Hood:**

* **SQLite database 💾💾💾:** Stores all your MES data securely. 
* **OPC UA communication 📡📡📡:** Talks directly to your machine for seamless data exchange. 
* **Object-Relational Mapping (ORM) 🔗🔗🔗:** Simplifies database interactions for developers. 

**Next Steps:**

This is a high-level overview of the MES design. We'll continue development and provide more details soon!

**Let's supercharge your production together! 🚀🚀🚀**

**Feel free to explore further sections using the handy Table of Contents below\!**

Markdown
# **A Supercharged MES for Your MPS Drilling Station** 🚀🚀🚀

## Table of Contents
* **[Key Features](#key-features)**
* **[User-Friendly Interface](#user-friendly-interface)**
* **[Under the Hood](#under-the-hood)**
* **[Next Steps](#next-steps)**

## Key Features
* **Real-time monitoring 👀👀👀:** Keep a **close eye** on your machine with live data.
* **Improved scheduling 🗓️🗓️🗓️:** Plan and optimize production schedules for **maximum efficiency**.
* **Enhanced decision-making 🧠🧠🧠:** Gain **valuable insights** from data to make **informed choices**.
* **Modular design 🧩🧩🧩:** Easily adapt the system to different stations with minimal changes. 

## User-Friendly Interface
* **Simple and intuitive UI 🧑‍💻🧑‍💻🧑‍💻:** Designed for all user types (operators, technicians, managers).
* **Operator window 👷‍♀️👷‍♀️👷‍♀️:** Submit work orders, monitor production status, and add new customers. 
* **Technician window 🔧🔧🔧:** View and manage downtime events (start/stop, reasons). 
* **Manager window 📊📊📊:** Generate reports, export data, and visualize Overall Equipment Effectiveness (OEE). 

## Under the Hood
* **SQLite database 💾💾💾:** Stores all your MES data securely. 
* **OPC UA communication 📡📡📡:** Talks directly to your machine for seamless data exchange. 
* **Object-Relational Mapping (ORM) 🔗🔗🔗:** Simplifies database interactions for developers. 

## Next Steps
This is a high-level overview of the MES design. We'll continue development and provide more details soon!

**Let's supercharge your production together! 🚀🚀🚀**

MES
```mermaid
graph TB
    %% Define the Database Package at the top
    subgraph "Database Package"
        DBConnection[Database Connection]
        CustomerTable[Customer Table/Object] --> DBConnection
        DowntimeTable[Downtime Table/Object] --> DBConnection
        EmployeeTable[Employee Table/Object] --> DBConnection
        OrderTable[Order Table/Object] --> DBConnection
        
        class DBConnection,CustomerTable,DowntimeTable,EmployeeTable,OrderTable innerGraph
    end
    
    %% Define the User Interface Package lower down
    subgraph "User Interface Package"
        MainWindow[Main Window] --> UserWindow
        UserWindow --> |inherits| MaintenanceWindow[Maintenance Window]
        UserWindow --> |inherits| ManagerWindow[Manager Window]
        UserWindow --> |inherits| OperatorWindow[Operator Window]
        MainWindow --> SignInWindow[Sign In Window]
        
        class MainWindow,UserWindow,MaintenanceWindow,ManagerWindow,OperatorWindow,SignInWindow innerGraph
    end
    
    %% Define the Analytics Package below User Interface
    subgraph "Analytics Package"
        OEECalc[OEE Calculator]
        ReportGen[Report Generator]
        OEECalc --> |analyzes| DowntimeTable
        OEECalc --> |analyzes| OrderTable
        ReportGen --> |generates| OrderTable
        ReportGen --> |generates| DowntimeTable
        
        class OEECalc,ReportGen innerGraph
    end
    
    %% Define the Communications Package below Analytics
    subgraph "Communications Package"
        OPCUAClient[OPCUA Client]
        CommsManager[Comms Manager]
        CommsManager --> OPCUAClient
        OPCUAClient --> |reads| OrderTable
        
        class CommsManager,OPCUAClient innerGraph
    end
    
    %% Connections between packages with labels
    SignInWindow --> |accesses| EmployeeTable
    OperatorWindow --> |manages| OrderTable
    OperatorWindow --> |accesses| CustomerTable
    MaintenanceWindow --> |logs| DowntimeTable
    ManagerWindow --> |views| EmployeeTable
    
    
    %% Styling adjustments for better readability
    classDef innerGraph fill:#f9f9f9,stroke:#333,stroke-width:2px
    style MainWindow fill:#e1f5fe,stroke:#333
    style DBConnection fill:#e8f5e9,stroke:#333
    style OEECalc fill:#fff3e0,stroke:#333
    style CommsManager fill:#fce4ec,stroke:#333
```

```mermaid
graph TB
    subgraph High Level
    UI[User Interface]
    end

    subgraph Mid Level
    AN[Analytics]
    DB[(Database)]
    end

    subgraph Low Level
    COM[Communications]
    end

    UI -->|Requests Data| DB
    UI -->|Requests Report| AN
    AN -->|Queries| DB
    AN -->|Returns Report| UI
    DB -->|Returns Data| UI
    DB -->|Returns Data| AN
    DB -->|Data Stream| COM
    COM -->|Updates| DB

    style DB fill:#f9f,stroke:#333,stroke-width:4px
    style UI fill:#bbf,stroke:#333,stroke-width:2px
    style AN fill:#ddf,stroke:#333,stroke-width:2px
    style COM fill:#fdd,stroke:#333,stroke-width:2px
```

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    EMPLOYEE ||--o{ DOWNTIME : reports
    EMPLOYEE }|--o{ ORDER : processes

    CUSTOMER {
        int customerid PK
        string customername
        string customeremail
        string customeraddress
    }

    ORDER {
        int orderId PK
        int customer_id FK
        int drilling_operation
        datetime order_date
        string status
        boolean passQualityControl
    }

    EMPLOYEE {
        int employeeId PK
        string name
        string username
        string password
        string role
    }

    DOWNTIME {
        int downtimeId PK
        int employeeId FK
        string downtimeReason
        datetime downtimeStart
        datetime downtimeEnd
        interval downtimeDelta
        string status
    }
```

```mermaid
classDiagram
    class NodeList {
        - _instance: NodeList
        - _nodes: list<Node>
        + new() NodeList
        + add_node(node: Node)
        + get_nodes() list<Node>
    }

    class Node {
        - ns_number: int
        - datablock: str
        - tag_name: str
        - address: str
        - past_value: bool
        - current_value: bool
        - rising_edge: bool
        + update_rising_edge()
        + write(value: Any)
    }

    class SubHandler {
        + datachange_notification(node: Node, val: Any, data: Any)
    }

    class PLC_COM {
        + init()
        + subscribe_nodes(node: Node, handler: SubHandler)
    }

    %% Relationships
    NodeList "1" *-- "0..*" Node : "stores"
    Node "1" --> "1" NodeList : "adds itself"
    SubHandler "1" --> "1" NodeList : "accesses"
    PLC_COM "1" --> "1" SubHandler : "uses for notifications"
    PLC_COM "1" --> "0..*" Node : "subscribes to"

    %% Descriptions
    class NodeList {
        <<singleton>> 
        Singleton class to store and manage nodes
    }

    class Node {
        Represents a data point, updates state, and writes to PLC
    }

    class SubHandler {
        Handles data changes and updates node state
    }

    class PLC_COM {
        Manages PLC communication and subscribes to nodes
    }
```
