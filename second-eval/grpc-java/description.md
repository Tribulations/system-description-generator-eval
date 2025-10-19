# grpc-java System Overview

## System Purpose
grpc-java is a Java implementation of gRPC, a high-performance, open-source universal RPC framework. It enables efficient communication between distributed services using HTTP/2 as the transport protocol, supporting multiple programming languages and providing features like authentication, load balancing, and observability.

## Key Components & Responsibilities

### Transport Layer
- **NettyClientHandler & NettyServerHandler**: Manage HTTP/2 frame processing for client and server connections using Netty
- **OkHttpClientTransport**: Alternative HTTP/2 transport implementation using OkHttp library
- **BinderTransport**: Android-specific IPC transport using Binder mechanism
- **InProcessTransport**: In-memory transport for testing and same-process communication

### Channel & Connection Management
- **Builder Classes**: Fluent API for configuring channels, servers, and credentials (ManagedChannelBuilder, ServerBuilder, various credential builders)
- **LoadBalancer Components**: Client-side load balancing with support for multiple policies (round-robin, weighted, etc.)
- **Connection Pooling**: Manages connection lifecycle, keep-alive, and reconnection logic

### Security & Authentication
- **TLS/SSL Support**: Certificate validation, mutual TLS, and custom trust managers
- **Credentials System**: Pluggable authentication (TlsChannelCredentials, InsecureChannelCredentials, CompositeCredentials)
- **RBAC & Authorization**: Role-based access control with policy matchers and authentication engines

### Observability & Monitoring
- **Census Integration**: OpenCensus-based metrics collection (ClientTracer, ServerTracer, CallAttemptsTracerFactory)
- **OpenTelemetry Support**: Modern observability with traces, metrics, and logs
- **Binary Logging**: Protocol-level logging for debugging and audit trails
- **Channelz**: Runtime introspection of channel and connection state

### Service Discovery & Routing
- **NameResolver**: DNS and custom service discovery mechanisms
- **RLS (Route Lookup Service)**: Dynamic routing based on request metadata
- **xDS Protocol**: Integration with service mesh control planes for advanced traffic management

### Protocol Handling
- **HTTP/2 Frame Processing**: Encoding/decoding of gRPC messages over HTTP/2 streams
- **Message Serialization**: Protobuf marshalling with support for custom serializers
- **Compression**: Pluggable compression (gzip, identity) for message payloads
- **Flow Control**: Stream and connection-level flow control management

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core implementation language
- **HTTP/2**: Transport protocol for all network communication
- **Protocol Buffers**: Default serialization format
- **Netty**: Primary network I/O framework for high-performance transport
- **OkHttp**: Alternative HTTP/2 client implementation

### Key Dependencies
- **OpenCensus/OpenTelemetry**: Observability and metrics collection
- **Guava**: Utility libraries for collections, concurrency, and functional programming
- **Android SDK**: Platform-specific components for Android (Binder transport)
- **Perfmark**: Low-overhead performance tracing
- **Envoy xDS APIs**: Service mesh integration protocols

### Security Libraries
- **Java SSL/TLS**: Native security providers
- **ALTS**: Application Layer Transport Security for Google Cloud
- **S2A**: Secure Session Agent for certificate management

## Architecture

### Layered Design
1. **Application Layer**: User-facing APIs (stubs, channels, servers)
2. **Interceptor Layer**: Cross-cutting concerns (authentication, logging, metrics)
3. **Transport Abstraction**: Protocol-agnostic stream and connection interfaces
4. **Transport Implementation**: Netty, OkHttp, Binder, or InProcess concrete implementations
5. **Network Layer**: HTTP/2 frame handling and socket management

### Component Interaction Pattern
- **Builder Pattern**: Extensive use for configuration objects
- **Factory Pattern**: Transport and credential creation
- **Observer Pattern**: State change notifications (connectivity, stream lifecycle)
- **Decorator Pattern**: Interceptors and forwarding implementations
- **Strategy Pattern**: Pluggable load balancing, name resolution, and compression

### Concurrency Model
- **Event Loop Architecture**: Netty-based non-blocking I/O
- **Synchronization Context**: Serialized execution for state management
- **Thread Pools**: Separate pools for application callbacks and transport operations
- **Lock-Free Structures**: Atomic operations and concurrent collections for high-throughput paths

## Data Flow

### Client Request Flow
1. **Application** creates stub and invokes RPC method
2. **ClientCall** applies interceptors (auth, metrics, retry)
3. **Channel** selects subchannel via load balancer
4. **Transport** serializes message and encodes as HTTP/2 frames
5. **Network** transmits frames over established connection
6. **Server Transport** receives frames and decodes messages
7. **ServerCall** dispatches to service implementation
8. **Response** flows back through same layers in reverse

### Connection Establishment
1. **NameResolver** resolves service name to addresses
2. **LoadBalancer** creates subchannels for resolved addresses
3. **Transport Factory** initiates connection (TLS handshake if configured)
4. **Protocol Negotiation** establishes HTTP/2 connection with settings exchange
5. **Keep-Alive Manager** maintains connection health with periodic pings

### Stream Lifecycle
1. **Stream Creation**: Allocate stream ID and initialize state
2. **Header Exchange**: Send/receive HTTP/2 HEADERS frames with metadata
3. **Message Transfer**: DATA frames with length-prefixed protobuf messages
4. **Flow Control**: WINDOW_UPDATE frames manage backpressure
5. **Stream Closure**: Half-close with END_STREAM flag, full close with trailers
6. **Resource Cleanup**: Deallocate buffers and update connection state

### Observability Data Flow
1. **Interceptors** capture call start/end events
2. **StreamTracers** record message counts and sizes
3. **StatsTraceContext** aggregates metrics per RPC
4. **Census/OpenTelemetry** exports to configured backends
5. **Binary Logger** writes protocol events to storage
6. **Channelz** maintains in-memory state for runtime queries