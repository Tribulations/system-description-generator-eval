# Accumulo System Overview

## 1. System Purpose
Apache Accumulo is a distributed, sorted key-value store built on top of Apache Hadoop. It provides robust, scalable data storage with cell-level access control, designed for handling large-scale data processing and querying operations.

## 2. Key Components & Responsibilities

### Core Server Components
- **Manager**: Orchestrates cluster operations, manages tablet assignments, coordinates compactions, handles table operations, and maintains cluster state. Implements load balancing and monitors tablet server health.
- **TabletServer**: Hosts tablets (partitions of tables), processes read/write operations, manages in-memory and on-disk data structures, handles compactions, and maintains write-ahead logs (WALs).
- **CompactionCoordinator**: Manages compaction scheduling and execution across the cluster.

### Client Components
- **Shell**: Interactive command-line interface for cluster administration and data operations. Supports table management, user operations, scanning, and system configuration.
- **TableOperationsImpl**: Implements client-side table operations including creation, deletion, configuration, compaction, splitting, and metadata retrieval.
- **FateOperationExecutor**: Executes Fault-Tolerant Executor (FATE) operations for distributed transactions.

### Data Management
- **RFile Writer/Reader**: Handles the proprietary RFile format for storing sorted key-value data with compression, encryption, and indexing capabilities.
- **TabletMetadata**: Manages metadata about tablets including location, files, logs, and operational state.
- **Ample**: Metadata table abstraction layer for accessing tablet metadata.

### Supporting Infrastructure
- **ServiceLock**: Distributed locking mechanism using ZooKeeper for coordination.
- **LiveTServerSet**: Tracks active tablet servers in the cluster.
- **EventCoordinator**: Manages cluster-wide events and notifications.

## 3. Core Technologies & Dependencies

### Primary Technologies
- **Apache Thrift**: RPC framework for inter-service communication
- **Apache Hadoop**: Underlying distributed file system (HDFS) and infrastructure
- **Apache ZooKeeper**: Distributed coordination and configuration management
- **Apache Commons**: Utility libraries (CLI, Collections, Lang)

### Key Libraries
- **Caffeine**: High-performance caching library
- **Guava**: Google's core Java libraries
- **SLF4J/Logback**: Logging framework
- **JLine**: Console input handling for the shell
- **Micrometer**: Metrics collection and monitoring

### Data Formats
- **BCFile**: Block-compressed file format
- **RFile**: Accumulo's native sorted key-value file format with bloom filters and indexes

## 4. Architecture

### Distributed Architecture
The system follows a master-worker architecture:
- **Manager Node**: Single active manager (with standby for HA) coordinates all cluster operations
- **TabletServer Nodes**: Multiple workers that store and serve data
- **Client Layer**: Applications interact through client APIs or the shell

### Data Organization
- **Tables**: Logical collections of key-value pairs
- **Tablets**: Horizontal partitions of tables distributed across tablet servers
- **Locality Groups**: Column families grouped together for optimized access patterns
- **RFiles**: Immutable sorted files storing tablet data

### Coordination Layer
- ZooKeeper maintains cluster state, configuration, and distributed locks
- FATE (Fault-Tolerant Executor) ensures atomic execution of distributed operations

## 5. Data Flow

### Write Path
1. Client sends mutations to TabletServer
2. TabletServer writes to in-memory structure and WAL simultaneously
3. When memory threshold reached, minor compaction flushes to RFile
4. Major compactions merge multiple RFiles periodically

### Read Path
1. Client issues scan request to TabletServer
2. TabletServer merges data from in-memory structures and RFiles
3. Iterators apply server-side filtering and transformations
4. Results streamed back to client in batches

### Metadata Flow
1. Client queries Manager for tablet locations
2. Manager consults metadata tables (root, metadata, user tables hierarchy)
3. Client caches tablet locations for subsequent operations
4. Cache invalidated on tablet migrations or splits

### Administrative Operations
1. Shell/Client submits operation to Manager
2. Manager creates FATE transaction for fault tolerance
3. FATE coordinates multi-step operations across cluster
4. Manager updates metadata and notifies affected TabletServers
5. TabletServers execute local changes (load/unload tablets, compactions)

### Compaction Flow
1. CompactionCoordinator schedules compactions based on policies
2. TabletServer receives compaction job
3. Reads input RFiles, merges sorted data, applies deletions
4. Writes new RFile, updates metadata
5. Old files marked for deletion after metadata update

This architecture ensures scalability, fault tolerance, and strong consistency while providing flexible data access patterns and security controls.