# Debezium Core System - High-Level Summary

## 1. System Purpose

Debezium Core is a change data capture (CDC) framework that monitors database changes and streams them as events to downstream consumers. It captures row-level changes (inserts, updates, deletes) from databases and transforms them into structured event streams, enabling real-time data integration and synchronization across distributed systems.

## 2. Key Components & Responsibilities

### Database Connectivity Layer
- **JdbcConnection**: Manages JDBC database connections with connection pooling, validation, and lifecycle management
- **ConnectionFactory & ConnectionFactoryDecorator**: Provide factory patterns for creating and decorating database connections
- **JdbcValueConverters**: Converts database-specific data types to Kafka Connect schema types

### Event Processing Pipeline
- **EventDispatcher**: Central coordinator that receives change events from sources and dispatches them to registered receivers
- **ChangeEventQueue**: Thread-safe bounded queue that buffers change events between producers and consumers
- **SnapshotReceiver & StreamingChangeRecordReceiver**: Handle events during initial snapshot and ongoing streaming phases

### Snapshot Management
- **RelationalSnapshotChangeEventSource**: Orchestrates initial database snapshots, reading existing table data
- **AbstractIncrementalSnapshotChangeEventSource**: Manages incremental snapshots that capture data changes without stopping streaming
- **SnapshotContext**: Maintains state and metadata during snapshot operations

### Signal Processing
- **SignalProcessor**: Processes control signals for operations like triggering snapshots or configuration changes
- **KafkaSignalChannel & FileSignalChannel**: Read signals from Kafka topics or file systems
- **SinkNotificationChannel**: Sends notifications about connector state and progress

### Schema Management
- **SchemaFactory**: Creates Kafka Connect schemas for source records, envelopes, and metadata
- **TableSchemaBuilder**: Builds schemas for relational tables with column mappings
- **RelationalDatabaseSchema**: Maintains schema metadata for relational databases

### Data Transformations
- **ExtractNewRecordState**: Single Message Transform (SMT) that extracts the new state from change events
- **TimezoneConverter**: Converts timestamp fields between timezones
- **ByLogicalTableRouter**: Routes records to different topics based on table names
- **OutboxEventRouter**: Implements the outbox pattern for transactional messaging

### Task Coordination
- **BaseSourceTask**: Base Kafka Connect SourceTask implementation managing connector lifecycle
- **ChangeEventSourceCoordinator**: Coordinates snapshot and streaming phases, handling transitions and error recovery

## 3. Core Technologies & Dependencies

### Primary Technologies
- **Apache Kafka Connect**: Framework for building source and sink connectors
- **JDBC**: Database connectivity standard for relational databases
- **Jackson**: JSON processing for serialization and configuration
- **SLF4J**: Logging facade with pluggable implementations

### Key Dependencies
- **Kafka Connect API**: Schema, SourceRecord, SourceTask, Transformation interfaces
- **Java SQL**: JDBC interfaces for database operations
- **Java Concurrency**: Locks, queues, atomic references for thread-safe operations
- **Java Time API**: Temporal types for timestamp handling

## 4. Architecture

### Layered Architecture
The system follows a layered architecture with clear separation of concerns:

**Layer 1 - Database Access**: JDBC connection management and query execution  
**Layer 2 - Change Capture**: Snapshot and streaming event sources  
**Layer 3 - Event Processing**: Dispatching, buffering, and transformation  
**Layer 4 - Integration**: Kafka Connect task implementation and signal handling

### Component Interaction Pattern
- **Producer-Consumer**: Change sources produce events, receivers consume them
- **Pipeline Pattern**: Events flow through dispatcher → queue → transformations → Kafka
- **Strategy Pattern**: Pluggable snapshot strategies, signal channels, and transformations
- **Factory Pattern**: Connection factories, schema factories, and event source factories

### Concurrency Model
- Thread-safe components use concurrent data structures (ConcurrentHashMap, LinkedBlockingQueue)
- ReentrantLocks protect critical sections during state transitions
- AtomicReferences manage shared state without blocking

## 5. Data Flow

### Initial Snapshot Flow
1. **ChangeEventSourceCoordinator** initiates snapshot phase
2. **RelationalSnapshotChangeEventSource** queries database tables
3. **JdbcConnection** executes SELECT queries with result set streaming
4. **SnapshotChangeRecordEmitter** creates change records for each row
5. **EventDispatcher** wraps records in envelopes with metadata
6. **ChangeEventQueue** buffers records for consumption
7. **BaseSourceTask** polls queue and returns records to Kafka Connect

### Streaming Change Flow
1. Database-specific streaming source (not in this core module) captures transaction logs
2. **StreamingChangeRecordReceiver** receives parsed change events
3. **EventDispatcher** enriches events with schema and metadata
4. **IncrementalSnapshotChangeEventSource** intercepts events to coordinate incremental snapshots
5. **ChangeEventQueue** buffers streaming records
6. **PostProcessors** apply custom transformations (e.g., ReselectColumnsPostProcessor)
7. **BaseSourceTask** delivers records to Kafka Connect framework

### Signal Processing Flow
1. **SignalChannelReader** (Kafka/File) reads signal payloads
2. **SignalProcessor** parses and validates signals
3. **SignalAction** implementations execute operations (snapshot, pause, resume)
4. **NotificationService** publishes status updates via notification channels

### Transformation Flow
1. Kafka Connect invokes **Transformation** implementations on records
2. **ExtractNewRecordState** unwraps change envelopes to extract payload
3. **TimezoneConverter** adjusts timestamp fields
4. **ByLogicalTableRouter** modifies topic names based on routing rules
5. Transformed records proceed to Kafka topics

### Metadata Flow
- **OffsetContext** tracks position in source database (LSN, binlog position)
- **Partition** identifies logical source partition
- **SchemaHistory** records DDL changes for schema evolution
- Offset and schema metadata persists in Kafka Connect offset and schema topics