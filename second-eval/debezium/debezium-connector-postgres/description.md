Here is a high-level summary of the `debezium-connector-postgres` system.

### 1. System Purpose
The system is a Debezium connector for Apache Kafka Connect. Its primary function is to perform Change Data Capture (CDC) on a PostgreSQL database, capturing row-level changes (INSERTs, UPDATEs, DELETEs) in real-time and streaming them as events to Apache Kafka topics.

### 2. Key Components & Responsibilities
*   **Connector & Task (`PostgresConnector`, `PostgresConnectorTask`):** These are the entry points for the Kafka Connect framework. They manage the connector's lifecycle, configuration, and task distribution.
*   **Connection Management (`PostgresConnection`, `PostgresReplicationConnection`):** Manages standard JDBC connections for schema discovery and snapshotting, and specialized replication connections to stream changes from PostgreSQL's logical decoding slot.
*   **Change Data Capture (`PostgresSnapshotChangeEventSource`, `PostgresStreamingChangeEventSource`):**
    *   The `Snapshot` source performs an initial consistent read of the database tables to capture the current state.
    *   The `Streaming` source connects to the replication stream to capture ongoing changes from the Write-Ahead Log (WAL) after the snapshot is complete.
*   **Message Decoding (`PgOutputMessageDecoder`, `PgProtoMessageDecoder`):** Decodes the binary replication protocol messages (e.g., from the `pgoutput` logical decoding plugin) into a structured format that the connector can process.
*   **Data Conversion & Schema Management (`PostgresValueConverter`, `TypeRegistry`, `PostgresSchema`):**
    *   `PostgresValueConverter` converts PostgreSQL-specific data types into Kafka Connect's data formats and schemas.
    *   `TypeRegistry` maintains a mapping of PostgreSQL types to their internal representations.
    *   `PostgresSchema` builds and maintains an in-memory representation of the database schema.
*   **Event Processing & Dispatching (`PostgresChangeEventSourceCoordinator`, `PostgresEventDispatcher`):**
    *   The `Coordinator` orchestrates the change capture process, managing the transition from the snapshot phase to the streaming phase.
    *   The `Dispatcher` processes logical change messages and creates `SourceRecord` objects to be sent to Kafka.
*   **State Management (`PostgresOffsetContext`):** Tracks the connector's position within the PostgreSQL WAL using the Log Sequence Number (LSN). This ensures that processing can resume from the correct point after a restart, preventing data loss or duplication.

### 3. Core Technologies & Dependencies
*   **Framework:** Apache Kafka Connect
*   **Core Library:** Debezium Core CDC Framework
*   **Database:** PostgreSQL (utilizing its logical decoding feature)
*   **Database Driver:** PostgreSQL JDBC Driver
*   **Logging:** SLF4J

### 4. Architecture
The system is designed as a plugin for the Apache Kafka Connect framework. Its architecture is event-driven and follows a two-phase pattern:
1.  **Snapshotting:** An initial, optional phase where the connector performs a consistent read of the database to capture a baseline of the data.
2.  **Streaming:** A continuous phase where the connector tails the PostgreSQL Write-Ahead Log (WAL) via a logical replication slot to capture and stream subsequent data changes in real-time.

This modular architecture separates concerns such as connection handling, data capture, message decoding, and event production.

### 5. Data Flow
1.  The `PostgresConnectorTask` initiates the data capture process, coordinated by the `PostgresChangeEventSourceCoordinator`.
2.  If a snapshot is required, `PostgresSnapshotChangeEventSource` connects via JDBC, reads the configured tables, and generates data records.
3.  Upon snapshot completion, `PostgresStreamingChangeEventSource` establishes a replication connection to the PostgreSQL server.
4.  PostgreSQL streams logical change events from the WAL to the connector.
5.  A `MessageDecoder` (e.g., `PgOutputMessageDecoder`) parses the binary stream into logical `ReplicationMessage` objects representing transactions and row changes.
6.  The `PostgresEventDispatcher` processes these messages, using `PostgresValueConverter` to transform PostgreSQL data types into Kafka Connect-compatible schemas and values.
7.  For each change, a `SourceRecord` is created, containing the before/after state of the row, source metadata (including the LSN), and the operation type (create, update, delete).
8.  The `PostgresOffsetContext` is updated with the LSN of the processed event.
9.  The generated `SourceRecord`s are handed off to the Kafka Connect framework, which writes them to the appropriate Kafka topics.