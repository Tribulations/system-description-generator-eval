# Debezium System Overview

## System Purpose
Debezium is a distributed platform for change data capture (CDC) that monitors databases and streams row-level changes to downstream consumers. It captures committed changes from database transaction logs and makes them available as event streams for real-time data integration, caching, search indexing, and analytics.

## Key Components & Responsibilities

### Core Pipeline Components
- **EventDispatcher**: Orchestrates the flow of change events from sources to consumers, manages schema changes, handles heartbeats, and coordinates with incremental snapshot sources
- **ChangeEventSourceCoordinator**: Coordinates snapshot and streaming phases, manages lifecycle transitions between different change event sources
- **BaseSourceTask**: Kafka Connect SourceTask implementation that manages connector lifecycle, state transitions, and record polling

### Database Connectors
- **BinlogStreamingChangeEventSource**: Captures MySQL/MariaDB changes from binary logs, handles replication events (INSERT, UPDATE, DELETE), manages GTID sets and binlog positions
- **PostgresConnection**: Manages PostgreSQL-specific connections, handles replication slots, type registry, and logical decoding
- **AbstractLogMinerStreamingChangeEventSource**: Oracle-specific streaming source using LogMiner for transaction log mining

### Snapshot Management
- **RelationalSnapshotChangeEventSource**: Executes initial consistent snapshots of database tables, supports parallel snapshotting and incremental snapshot windows
- **AbstractIncrementalSnapshotChangeEventSource**: Implements incremental snapshotting for capturing table data without blocking writes, uses watermarking for consistency
- **MongoDbIncrementalSnapshotChangeEventSource**: MongoDB-specific incremental snapshot implementation

### Data Access & Transformation
- **JdbcConnection**: Generic JDBC connection wrapper providing query execution, metadata access, and connection lifecycle management
- **JdbcValueConverters**: Converts JDBC types to Kafka Connect schema types, handles temporal types, binary data, and special values
- **PostgresValueConverter**: PostgreSQL-specific type conversions including arrays, JSON, geometric types, and custom types

### Schema & History Management
- **KafkaSchemaHistory**: Persists database schema changes to Kafka topics for recovery and consistency
- **Builder** (multiple contexts): Implements builder pattern for constructing complex objects like predicates, schemas, and configurations across various components

### Event Conversion & Serialization
- **CloudEventsConverter**: Converts Debezium change events to CloudEvents format for standardized event representation
- **CESchemaBuilder**: Builds CloudEvents-compliant schemas for change event serialization

### JDBC Utilities
- **ConnectionFactory/ConnectionFactoryDecorator**: Factory pattern for creating and decorating database connections
- **Operations**: Encapsulates common JDBC operations with error handling and resource management
- **ResultSetExtractor/ResultSetConsumer/ResultSetMapper**: Functional interfaces for processing JDBC ResultSets with various consumption patterns

### Async Engine (Embedded Mode)
- **AsyncEmbeddedEngine**: Asynchronous embedded Debezium engine for running connectors without Kafka Connect
- **SourceRecordCommitter/ConvertingRecordCommitter**: Manages offset commits and record conversion in embedded mode
- **PollRecords**: Handles asynchronous record polling with retry logic

### Dialect Support
- **GeneralDatabaseDialect**: Provides database-specific SQL generation, type mapping, and DDL operations for JDBC sink connector

### Transformation
- **NewRecordValueMetadata**: SMT (Single Message Transform) for extracting and enriching record metadata

## Core Technologies & Dependencies

### Primary Technologies
- **Apache Kafka & Kafka Connect**: Event streaming platform and connector framework
- **JDBC**: Database connectivity standard
- **MySQL Binlog Client** (shyiko): Binary log event processing
- **PostgreSQL JDBC Driver**: PostgreSQL-specific features including replication protocol
- **MongoDB Java Driver**: MongoDB change stream processing

### Key Libraries
- **Apache Kafka Connect API**: SourceTask, SourceRecord, Converter interfaces
- **Jackson**: JSON processing and serialization
- **SLF4J**: Logging facade
- **Hibernate ORM**: Used in JDBC sink dialect for type mapping
- **Chicory WASM Runtime**: WebAssembly support for scripting transforms

### Supported Databases
- MySQL/MariaDB (via binlog)
- PostgreSQL (via logical replication)
- Oracle (via LogMiner)
- MongoDB (via change streams)
- SQL Server, Db2, Cassandra (implied by architecture)

## Architecture

### Layered Architecture
1. **Connector Layer**: Database-specific implementations (MySQL, PostgreSQL, Oracle, MongoDB)
2. **Pipeline Layer**: Generic CDC pipeline components (EventDispatcher, ChangeEventSourceCoordinator)
3. **Source Layer**: Snapshot and streaming change event sources
4. **Schema Layer**: Schema management, history tracking, and evolution
5. **Transformation Layer**: SMTs and converters for event format transformation
6. **Integration Layer**: Kafka Connect integration and embedded engine support

### Design Patterns
- **Factory Pattern**: ConnectionFactory, StatementFactory for object creation
- **Builder Pattern**: Extensive use for complex object construction (Builder class with multiple build() signatures)
- **Strategy Pattern**: Different snapshot strategies, value converters per database
- **Decorator Pattern**: ConnectionFactoryDecorator for connection enhancement
- **Template Method**: AbstractSnapshotChangeEventSource, AbstractIncrementalSnapshotChangeEventSource

### Concurrency Model
- **Single-threaded event processing**: Annotated with @SingleThreadAccess
- **Thread-safe components**: JdbcConnection, various utilities marked @ThreadSafe
- **Async execution**: ExecutorService-based parallel snapshot processing
- **Lock-based coordination**: ReentrantLock for state management in BaseSourceTask

## Data Flow

### Initial Snapshot Phase
1. **BaseSourceTask** starts and initializes connector configuration
2. **ChangeEventSourceCoordinator** triggers snapshot phase
3. **RelationalSnapshotChangeEventSource** creates snapshot connection and locks tables
4. **JdbcConnection** queries table metadata and row data
5. **JdbcValueConverters** converts database types to Kafka Connect types
6. **EventDispatcher** receives snapshot records and dispatches to Kafka Connect
7. **KafkaSchemaHistory** records initial schema state

### Streaming Phase
1. **BinlogStreamingChangeEventSource** (MySQL) or **PostgresConnection** (PostgreSQL) connects to transaction log
2. Log events are parsed into **LogMinerEventRow** or binlog events
3. **ChangeRecordEmitter** creates change records with before/after states
4. **EventDispatcher** enriches events with transaction metadata
5. **CloudEventsConverter** optionally transforms to CloudEvents format
6. Records flow to Kafka Connect framework for delivery to Kafka topics

### Incremental Snapshot Phase
1. **SignalProcessor** receives incremental snapshot signal
2. **AbstractIncrementalSnapshotChangeEventSource** chunks table data
3. Watermarks inserted into stream to track snapshot boundaries
4. Snapshot chunks interleaved with streaming events
5. **WatermarkWindowCloser** ensures consistency between snapshot and streaming data

### Schema Change Handling
1. DDL events detected in transaction log
2. **SchemaChangeEvent** created with DDL statement
3. **KafkaSchemaHistory** persists schema change to history topic
4. **DatabaseSchema** updates in-memory schema representation
5. **EventDispatcher** emits schema change event to dedicated topic

### Embedded Mode Flow
1. **AsyncEmbeddedEngine** initializes without Kafka Connect runtime
2. **EngineSourceTask** polls connector for SourceRecords
3. **ConvertingRecordCommitter** converts and commits records
4. **OffsetBackingStore** (file/memory/Kafka) persists offsets
5. Consumer receives records via callback interface