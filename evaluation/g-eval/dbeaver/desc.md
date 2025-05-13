System Description: Here's a structured high-level summary of the DBeaver system based on the provided code:

**1. System Purpose:**
DBeaver is a database management and SQL development tool that provides a unified interface for working with various database systems. It enables users to write SQL queries, view and manipulate data, and manage database connections.

**2. Key Components & Responsibilities:**

- **ResultSetViewer:**
  - Handles the display and manipulation of database query results
  - Manages data presentation, filtering, and editing capabilities
  - Controls the user interface for data visualization

- **SQLEditor:**
  - Provides SQL query editing and execution functionality
  - Manages database connections and query processing
  - Handles result set presentation and multiple result tabs

- **DataSourceDescriptor:**
  - Manages database connection configurations and credentials
  - Handles connection lifecycle (connect, disconnect, reconnect)
  - Provides security and authentication management

**3. Core Technologies & Dependencies:**

Primary Technologies:
- Java (Core language)
- Eclipse Platform (RCP framework)
- SWT/JFace (UI framework)

Key Dependencies:
- Eclipse Core Runtime
- Eclipse UI components
- Database-specific JDBC drivers
- Core Java utilities and IO libraries

Framework Integration:
- Uses Eclipse's extension point system
- Implements Eclipse's editor and viewer frameworks
- Integrates with Eclipse's workspace and project system

The system follows a plugin-based architecture typical of Eclipse RCP applications, with clear separation between UI components, data handling, and database connectivity layers. It emphasizes security through credential management and supports multiple database platforms through an abstracted connection management system.