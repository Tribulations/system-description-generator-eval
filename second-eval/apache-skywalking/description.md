# Apache SkyWalking OAP Server - System Overview

## System Purpose
Apache SkyWalking OAP (Observability Analysis Platform) Server is a distributed tracing and application performance monitoring backend system. It collects, processes, analyzes, and stores observability data from distributed systems, providing metrics aggregation, trace analysis, logging, and profiling capabilities for microservices architectures.

## Key Components & Responsibilities

### Core Module (`org.apache.skywalking.oap.server.core`)
- **CoreModuleProvider**: Bootstraps the entire OAP server, initializing all subsystems including storage, query services, analysis workers, and remote communication
- **Metrics System**: Processes and aggregates performance metrics with downsampling support (minute, hour, day)
- **Source Receiver**: Ingests observability data from various sources (traces, logs, metrics, events)
- **Query Services**: Provides data retrieval APIs for topology, traces, metrics, logs, alarms, and metadata
- **Worker System**: Manages data processing pipelines using stream processors for records, metrics, and top-N aggregations

### Storage Layer (`org.apache.skywalking.oap.server.storage.plugin.*`)
- **Multi-Backend Support**: Pluggable storage implementations for Elasticsearch, BanyanDB, and JDBC databases
- **Schema Management**: Handles data model creation, indexing strategies, and TTL policies
- **Query DAOs**: Provides specialized data access objects for different query patterns (traces, metrics, logs, topology)

### Receiver Modules
- **eBPF Receiver** (`org.apache.skywalking.oap.server.receiver.ebpf`): Collects kernel-level profiling data and network metrics from eBPF probes
- **Browser Receiver**: Processes frontend performance and error data
- **Zabbix Receiver**: Integrates monitoring data from Zabbix agents
- **Zipkin Compatibility**: Supports Zipkin trace format ingestion

### Query & API Layer
- **GraphQL API**: Primary query interface for UI and external clients
- **PromQL Support** (`org.apache.skywalking.oap.query.promql`): Prometheus-compatible query language for metrics
- **Zipkin Query API**: Provides Zipkin-compatible trace query endpoints
- **Debugging Interface**: Exposes internal query execution details for troubleshooting

### Analysis & Processing
- **Meter System**: Processes custom metrics using DSL-based rules
- **OAL Engine**: Domain-specific language for defining metrics aggregation rules
- **Profiling Services**: Manages CPU profiling tasks (async profiler, eBPF, continuous profiling)
- **Topology Analysis**: Builds service dependency graphs and relationship metrics

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core implementation language
- **gRPC**: High-performance RPC framework for agent communication
- **Protocol Buffers**: Data serialization format
- **Armeria**: HTTP/2 server framework for REST APIs
- **Netty**: Asynchronous network communication

### Storage Technologies
- **Elasticsearch**: Primary time-series and document storage backend
- **BanyanDB**: Purpose-built observability database
- **JDBC**: Relational database support (MySQL, PostgreSQL, H2)

### Data Processing
- **Groovy DSL**: Dynamic rule evaluation for metrics and log analysis
- **ANTLR**: Parser generation for PromQL and OAL languages
- **Guava**: Utility libraries for collections and caching

### Supporting Libraries
- **Lombok**: Reduces boilerplate code
- **Gson/Jackson**: JSON serialization
- **Kubernetes Client**: Service discovery and metadata enrichment
- **Kafka**: Optional message queue for data ingestion

## Architecture

### Layered Architecture
```
┌─────────────────────────────────────────────────────┐
│  Query Layer (GraphQL, REST, PromQL, Zipkin APIs)  │
├─────────────────────────────────────────────────────┤
│  Service Layer (Query Services, Profiling, Cache)  │
├─────────────────────────────────────────────────────┤
│  Analysis Layer (OAL Engine, Metrics Aggregation)  │
├─────────────────────────────────────────────────────┤
│  Processing Layer (Stream Workers, Batch Processors)│
├─────────────────────────────────────────────────────┤
│  Receiver Layer (gRPC, HTTP, Kafka Consumers)      │
├─────────────────────────────────────────────────────┤
│  Storage Layer (ES, BanyanDB, JDBC Adapters)       │
└─────────────────────────────────────────────────────┘
```

### Module System
The system uses a modular architecture where each module (`ModuleProvider`) declares dependencies and services. The `CoreModule` acts as the central coordinator, with specialized modules for storage, receivers, and query handling.

### Clustering & Distribution
- **Remote Communication**: gRPC-based inter-node communication for distributed deployments
- **Worker Distribution**: Load balancing across cluster nodes using consistent hashing
- **Cluster Coordination**: Service discovery and health checking via cluster module

## Data Flow

### Ingestion Pipeline
1. **Data Reception**: Agents send telemetry data via gRPC to receiver handlers
2. **Source Generation**: Raw data is converted to typed `Source` objects (Service, ServiceInstance, Endpoint, etc.)
3. **Stream Processing**: Sources are dispatched to appropriate `StreamProcessor` implementations
4. **Aggregation**: Metrics are aggregated using time-bucketed windows with downsampling
5. **Persistence**: Processed data is batched and written to storage backends

### Query Pipeline
1. **API Request**: Client queries via GraphQL, REST, or PromQL endpoints
2. **Service Layer**: Query services validate parameters and coordinate data retrieval
3. **DAO Layer**: Storage-specific DAOs execute optimized queries
4. **Result Assembly**: Raw storage results are transformed into domain objects
5. **Response**: Formatted data is returned to the client

### Profiling Data Flow
1. **Task Creation**: Profiling tasks are created via mutation services
2. **Task Distribution**: Tasks are pushed to agents via command service
3. **Data Collection**: Agents upload profiling data (stack traces, eBPF events)
4. **Analysis**: Profiling analyzer processes raw data into flame graphs and aggregations
5. **Storage & Query**: Analyzed data is stored and made available through query services

### Metrics Processing
1. **Meter Data**: Custom metrics arrive via meter receiver or OTel protocol
2. **DSL Evaluation**: Metrics are processed through configurable DSL rules
3. **Entity Resolution**: Metrics are associated with services, instances, or endpoints
4. **Aggregation**: Time-series aggregation with configurable functions (sum, avg, percentile)
5. **Downsampling**: Automatic rollup to hourly and daily granularities

### Topology Construction
1. **Relationship Sources**: Service/instance/endpoint relationships are extracted from traces
2. **Graph Building**: Dependency graphs are constructed from relationship metrics
3. **Layer Detection**: Services are classified by technology layer (database, cache, MQ, etc.)
4. **Metric Attachment**: Performance metrics are attached to topology nodes and edges