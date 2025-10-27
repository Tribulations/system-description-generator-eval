# Interlok System Overview

## System Purpose
Interlok is an enterprise integration platform designed to facilitate message-based data transformation and routing between heterogeneous systems. It provides a flexible framework for consuming messages from various sources, applying transformations and business logic, and producing outputs to multiple destinations.

## Key Components & Responsibilities

### Core Message Processing
- **AdaptrisMessage**: Central data structure representing messages flowing through the system, containing payload, metadata, and object headers
- **ServiceImp & ServiceCollection**: Execute business logic and transformations on messages in sequential or conditional workflows
- **Workflow (WorkflowImp)**: Orchestrates message consumption, service execution, and message production within channels
- **Channel**: Logical grouping of workflows with shared error handling and connection management

### Connectivity & Transport
- **AdaptrisConnection**: Abstract connection management for various protocols (JMS, JDBC, HTTP, FTP/SFTP, File System)
- **JmsConnection**: JMS messaging integration with vendor-specific implementations via JNDI
- **DatabaseConnection**: JDBC database connectivity with connection pooling and transaction support
- **FileTransferConnection**: FTP/SFTP file transfer operations with session caching
- **HttpProducer/Consumer**: RESTful HTTP communication with OAuth authentication support

### Message Transformation
- **XmlTransformService**: XSLT-based XML transformations with caching
- **XPathService**: XPath-based data extraction and manipulation
- **MimeEncoder/Aggregator**: MIME multipart message handling
- **MessageTypeTranslator**: Protocol-specific message format conversion (e.g., JMS to Interlok)

### Data Access & Persistence
- **JdbcService**: SQL query execution and result set processing
- **JdbcDataQueryService**: Database queries with XML/JSON result formatting
- **JdbcStoredProcedureProducer**: Stored procedure invocation with parameter binding
- **ResultSetTranslator**: Converts JDBC result sets to message payloads

### Runtime Management
- **AdapterManager**: JMX-based runtime management and monitoring
- **WorkflowManager/ChannelManager**: Component lifecycle and state management
- **AdapterRegistry**: Central registry for adapter instances and management components
- **BootstrapProperties**: Configuration loading and system initialization

### Error Handling & Retry
- **FailedMessageRetrier**: Configurable retry mechanisms for failed messages
- **RetryFromJetty**: HTTP-based retry interface with filesystem/JDBC persistence
- **ProcessingExceptionHandler**: Channel-level error handling strategies

### HTTP Server Integration
- **JettyMessageConsumer**: Embedded Jetty server for HTTP endpoint exposure
- **JettyRouteCondition**: URL pattern and HTTP method-based routing
- **JettyServerManager**: Servlet container lifecycle management

## Core Technologies & Dependencies

### Frameworks & Libraries
- **XStream**: XML/JSON serialization and configuration marshalling
- **Apache Commons**: Utilities (IO, Lang3, Collections)
- **Jetty**: Embedded HTTP server and servlet container
- **Quartz Scheduler**: Cron-based polling and scheduled tasks
- **JSch**: SFTP client implementation
- **Apache Commons Net**: FTP client operations

### Standards & Protocols
- **JMS (Java Message Service)**: Message-oriented middleware integration
- **JDBC**: Relational database connectivity
- **HTTP/HTTPS**: RESTful web services
- **MIME**: Multipart message encoding
- **XSLT/XPath**: XML processing and transformation

### Management & Monitoring
- **JMX (Java Management Extensions)**: Runtime monitoring and control
- **SLF4J/Logback**: Logging framework
- **Lombok**: Boilerplate code reduction

## Architecture

### Layered Structure
1. **Configuration Layer**: XStream-based XML/JSON configuration with annotation-driven metadata
2. **Runtime Layer**: Component lifecycle management, state machines, and JMX exposure
3. **Service Layer**: Pluggable service implementations for transformation and routing
4. **Connection Layer**: Protocol-specific adapters with connection pooling
5. **Transport Layer**: Message producers and consumers for various protocols

### Component Lifecycle
All components follow a standardized lifecycle: `Init → Start → Stop → Close` managed by `LifecycleHelper` with state tracking via `ComponentState`.

### Extensibility Model
- **ServiceImp**: Base class for custom service implementations
- **AdaptrisConnection**: Abstract connection framework
- **MessageTypeTranslator**: Protocol-specific message conversion
- **VendorImplementation**: JMS vendor-specific adaptations

## Data Flow

### Standard Message Processing Pipeline
1. **Consumption**: `AdaptrisMessageConsumer` receives messages from external systems (JMS queue, HTTP request, file system, database poll)
2. **Workflow Entry**: Message enters `Workflow` with metadata enrichment (source identifiers, timestamps)
3. **Service Execution**: Sequential processing through `ServiceCollection` with conditional branching support
4. **Transformation**: Services apply business logic (XSLT, database lookups, content manipulation)
5. **Production**: `AdaptrisMessageProducer` delivers transformed messages to target systems
6. **Error Handling**: Failed messages route to `ProcessingExceptionHandler` or `FailedMessageRetrier`

### Key Data Structures
- **Metadata**: Key-value pairs for routing decisions and audit trails
- **Object Headers**: Typed objects for inter-service communication
- **Message Events**: Lifecycle tracking for monitoring and debugging

### Concurrency Model
- **Pooled Workflows**: Thread pools for parallel message processing (`PoolingWorkflow`)
- **Service Workers**: Reusable service instances via Apache Commons Pool
- **Connection Sharing**: Shared connections across workflows within channels

### Configuration Resolution
- **External Resolvers**: Password decryption and property substitution at runtime
- **JNDI Integration**: Shared component lookup via naming context
- **Dynamic Properties**: Metadata-driven configuration overrides

This architecture enables flexible integration patterns including message routing, content-based routing, protocol bridging, batch processing, and event-driven workflows while maintaining separation of concerns and operational manageability.