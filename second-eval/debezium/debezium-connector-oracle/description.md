# Debezium Oracle Connector - System Overview

## 1. System Purpose

The **debezium-connector-oracle** is a change data capture (CDC) connector that monitors Oracle databases and streams database changes as events to Apache Kafka. It captures INSERT, UPDATE, DELETE, and DDL operations in real-time, enabling downstream systems to react to database changes without impacting the source database performance.

## 2. Key Components & Responsibilities

### Streaming Adapters
- **LogMiner Adapters** (`BufferedLogMinerAdapter`, `UnbufferedLogMinerAdapter`): Use Oracle's LogMiner API to read redo logs and extract change events. Buffered version caches transactions for better handling of large transactions.
- **XStream Adapter** (`XStreamAdapter`): Uses Oracle XStream API as an alternative CDC mechanism for Oracle databases.
- **OpenLogReplicator Adapter** (`OpenLogReplicatorAdapter`): Integrates with OpenLogReplicator, an open-source Oracle CDC tool.

### Transaction Management
- **Transaction Caches** (`LogMinerTransactionCache`, `MemoryLogMinerTransactionCache`, `InfinispanLogMinerTransactionCache`, `EhcacheLogMinerTransactionCache`): Store in-flight transactions and their events. Support multiple storage backends (in-memory, Infinispan, Ehcache) for scalability.
- **Transaction Objects** (`Transaction`, `AbstractTransaction`, `InfinispanTransaction`, `EhcacheTransaction`): Represent database transactions with metadata (SCN, transaction ID, timestamps, events).

### Event Processing
- **Event Types** (`LogMinerEvent`, `DmlEvent`, `TruncateEvent`, `LobWriteEvent`, `XmlBeginEvent`, etc.): Represent different types of database operations including standard DML, LOB operations, and XML data handling.
- **Event Emitters** (`LogMinerChangeRecordEmitter`, `XStreamChangeRecordEmitter`, `OpenLogReplicatorChangeRecordEmitter`): Convert database events into Debezium change records for Kafka.
- **Event Parsers** (`LogMinerDmlParser`, `LogMinerColumnResolverDmlParser`): Parse Oracle redo SQL statements into structured event data.

### Schema Management
- **OracleDatabaseSchema**: Manages table schemas, handles DDL changes, and maintains schema history.
- **OracleDdlParser**: Parses Oracle DDL statements using ANTLR-generated parsers to track schema evolution.
- **Value Converters** (`OracleValueConverters`, `OpenLogReplicatorValueConverter`): Convert Oracle-specific data types to Kafka Connect schema types.

### Offset & Position Tracking
- **OracleOffsetContext**: Tracks the connector's position in the Oracle redo logs using System Change Numbers (SCN) and transaction metadata.
- **CommitScn**: Manages commit SCNs across multiple redo threads in RAC environments.
- **LcrPosition**: Tracks position for XStream-based replication.

### Connection & Session Management
- **OracleConnection**: Extends JdbcConnection to provide Oracle-specific database operations including SCN retrieval, redo thread state queries, and session management.
- **LogMinerSessionContext**: Manages LogMiner sessions, including starting/stopping mining sessions and log file registration.

### Snapshot Processing
- **OracleSnapshotChangeEventSource**: Handles initial snapshot of database tables before starting incremental change capture.
- **OracleSignalBasedIncrementalSnapshotChangeEventSource**: Supports incremental snapshots triggered by signals.

### Metrics & Monitoring
- **LogMinerStreamingChangeEventSourceMetrics**: Tracks performance metrics including batch processing times, transaction counts, and SCN progression.
- **OpenLogReplicatorStreamingChangeEventSourceMetrics**: Metrics specific to OpenLogReplicator adapter.

## 3. Core Technologies & Dependencies

### Primary Technologies
- **Apache Kafka Connect**: Framework for building connectors
- **Oracle JDBC Driver**: Database connectivity
- **Oracle LogMiner API**: Primary CDC mechanism
- **Oracle XStream API**: Alternative CDC mechanism
- **ANTLR**: Parser generation for DDL parsing

### Caching Technologies
- **Infinispan**: Distributed cache (embedded and remote modes)
- **Ehcache**: Local caching solution
- **In-Memory Maps**: Simple HashMap-based caching

### Serialization
- **Protocol Buffers** (via Infinispan Protostream): For distributed cache serialization
- **Custom Serializers**: For Ehcache persistence

### Supporting Libraries
- **SLF4J**: Logging abstraction
- **Jackson**: JSON processing (for OpenLogReplicator)
- **Debezium Core**: Base connector framework

## 4. Architecture

### Layered Architecture

**Connector Layer** (`OracleConnector`, `OracleConnectorTask`)
- Manages connector lifecycle and configuration
- Delegates to appropriate streaming adapter based on configuration

**Adapter Layer** (`StreamingAdapter` implementations)
- Abstracts different CDC mechanisms (LogMiner, XStream, OpenLogReplicator)
- Provides unified interface for change event streaming

**Event Source Layer** (`StreamingChangeEventSource` implementations)
- Executes the actual CDC logic
- Reads from Oracle redo logs or streams
- Manages transaction boundaries and event ordering

**Buffering Layer** (`CacheProvider`, `LogMinerCache`, `LogMinerTransactionCache`)
- Handles transaction buffering with pluggable storage backends
- Manages memory pressure and eviction policies

**Parsing Layer** (`LogMinerDmlParser`, `OracleDdlParser`)
- Parses redo SQL and DDL statements
- Extracts structured data from Oracle-specific formats

**Schema Layer** (`OracleDatabaseSchema`, `OracleValueConverters`)
- Maintains current schema state
- Handles type conversions and schema evolution

**Offset Management Layer** (`OracleOffsetContext`, `CommitScn`)
- Tracks connector position for fault tolerance
- Manages multi-threaded redo log positions in RAC

## 5. Data Flow

### Initial Snapshot Flow
1. **OracleSnapshotChangeEventSource** queries all configured tables
2. Reads current SCN from database
3. Emits snapshot records for each table row
4. Stores final snapshot SCN in offset context
5. Transitions to streaming mode

### Streaming Change Capture Flow (LogMiner)

**Log Mining Setup**
1. **LogMinerSessionContext** starts LogMiner session
2. Registers redo log files based on SCN range
3. Configures mining query with table filters

**Event Processing**
1. **BufferedLogMinerStreamingChangeEventSource** queries LogMiner view
2. Reads **LogMinerEventRow** records from redo logs
3. Parses redo SQL using **LogMinerDmlParser**
4. Creates **LogMinerEvent** objects (DmlEvent, LobWriteEvent, etc.)
5. Buffers events in **LogMinerTransactionCache** until commit

**Transaction Commit**
1. **TransactionCommitConsumer** receives commit event
2. Retrieves all events for transaction from cache
3. Processes LOB fragments and multi-part events
4. Emits events via **LogMinerChangeRecordEmitter**
5. **EventDispatcher** sends records to Kafka
6. Updates **OracleOffsetContext** with commit SCN
7. Removes transaction from cache

**Offset Persistence**
1. Kafka Connect framework periodically calls `getOffset()`
2. **OracleOffsetContext** serializes current SCN and transaction state
3. Offset stored in Kafka Connect offset storage
4. Used for restart/recovery scenarios

### XStream Flow
1. **XstreamStreamingChangeEventSource** connects to XStream outbound server
2. Receives **LCR** (Logical Change Records) from Oracle
3. **LcrEventHandler** processes each LCR
4. **XStreamChangeRecordEmitter** converts to Debezium format
5. Updates **LcrPosition** for offset tracking

### OpenLogReplicator Flow
1. **OlrNetworkClient** connects to OpenLogReplicator via TCP
2. Receives **StreamingEvent** objects as JSON
3. **OpenLogReplicatorChangeRecordEmitter** processes events
4. Tracks position using checkpoint SCN

### Schema Change Handling
1. DDL events detected in redo logs or streams
2. **OracleSchemaChangeEventEmitter** parses DDL using **OracleDdlParser**
3. **OracleDatabaseSchema** updates internal schema representation
4. Schema change event emitted to Kafka schema change topic
5. Subsequent DML events use updated schema

### Error Handling & Recovery
1. **OracleErrorHandler** catches SQL exceptions
2. Retryable errors (e.g., `SQLRecoverableException`) trigger reconnection
3. Non-retryable errors stop connector
4. On restart, connector reads last committed offset
5. Resumes from stored SCN position