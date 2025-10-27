# Jedis System Overview

## System Purpose
Jedis is a Java client library for Redis, providing a comprehensive interface for interacting with Redis servers. It enables Java applications to execute Redis commands, manage connections, and handle various Redis data structures and features including clustering, sentinel-based failover, and client-side caching.

## Key Components & Responsibilities

### Connection Management
- **Connection**: Core class handling socket-level communication with Redis servers, managing protocol serialization/deserialization
- **ConnectionPool**: Apache Commons Pool2-based connection pooling for resource management
- **ConnectionFactory**: Factory pattern implementation for creating and validating connection instances
- **JedisSocketFactory**: Abstracts socket creation with SSL/TLS support

### Client Implementations
- **UnifiedJedis**: Base client providing unified command execution interface
- **Jedis**: Standard standalone Redis client with direct command execution
- **JedisPooled**: Pooled connection variant for high-concurrency scenarios
- **JedisCluster**: Cluster-aware client with automatic slot-based routing
- **JedisSentineled**: Sentinel-based high-availability client with automatic failover
- **MultiDbClient**: Multi-database client with circuit breaker and failover capabilities

### Command Execution
- **CommandObjects**: Command builder generating CommandObject instances for all Redis operations
- **CommandExecutor**: Interface defining command execution strategy
- **ClusterCommandExecutor**: Cluster-specific executor handling redirections and slot migrations
- **MultiDbCommandExecutor**: Multi-database executor with resilience patterns

### Protocol & Serialization
- **Protocol**: Redis protocol (RESP) implementation handling command encoding and response parsing
- **CommandArguments**: Type-safe command argument builder
- **Builder/BuilderFactory**: Response deserialization framework converting raw Redis responses to Java objects

### High Availability & Resilience
- **MultiDbConnectionProvider**: Multi-database connection provider with health checking and failover
- **Database**: Represents individual database endpoints with circuit breaker and retry logic
- **HealthCheck/HealthCheckImpl**: Proactive health monitoring for database endpoints
- **SentineledConnectionProvider**: Sentinel-based connection provider with master discovery

### Pipelining & Transactions
- **Pipeline**: Batched command execution without waiting for individual responses
- **Transaction**: MULTI/EXEC transaction support with atomic command execution
- **AbstractPipeline/AbstractTransaction**: Base classes providing common pipelining functionality

### Client-Side Caching
- **CacheConnection**: Connection wrapper integrating client-side cache
- **Cache/AbstractCache**: Cache interface and implementation for storing command responses
- **CacheEntry**: Cached value container with metadata

### Module Support
- **RediSearch**: Full-text search capabilities (Query, AggregationBuilder, SearchResult)
- **RedisJSON**: JSON document operations
- **RedisTimeSeries**: Time-series data management
- **RedisBloom**: Probabilistic data structures (Bloom filters, Cuckoo filters)

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core implementation language
- **Redis Protocol (RESP)**: Binary protocol for Redis communication
- **Apache Commons Pool2**: Connection pooling infrastructure

### Resilience Libraries
- **Resilience4j**: Circuit breaker, retry, and fallback patterns for multi-database failover

### Serialization
- **JSON (org.json)**: JSON parsing for RedisJSON module responses
- **GSON**: Alternative JSON processing for REST API interactions

### Security
- **javax.net.ssl**: SSL/TLS support for encrypted connections
- **Authentication**: Token-based authentication with AuthXManager

### Logging
- **SLF4J**: Logging facade for diagnostic output

## Architecture

### Layered Architecture
1. **Command Interface Layer**: Type-safe command interfaces (JedisCommands, PipelineCommands, etc.)
2. **Client Layer**: Client implementations (Jedis, JedisCluster, MultiDbClient)
3. **Execution Layer**: Command executors with routing and resilience logic
4. **Connection Layer**: Connection management, pooling, and protocol handling
5. **Transport Layer**: Socket communication with SSL/TLS support

### Design Patterns
- **Builder Pattern**: Client configuration (ClientBuilder hierarchy)
- **Factory Pattern**: Connection and object creation
- **Strategy Pattern**: Command execution strategies (standalone, cluster, multi-db)
- **Decorator Pattern**: Connection wrapping for caching (CacheConnection)
- **Template Method**: Pipeline and transaction base classes

### Multi-Database Architecture
The multi-database implementation uses:
- **Circuit Breaker**: Prevents cascading failures across databases
- **Retry Logic**: Automatic retry with exponential backoff
- **Health Probing**: Continuous health monitoring with configurable policies
- **Graceful Degradation**: Fallback to secondary databases on primary failure

## Data Flow

### Standard Command Execution
1. Client method invocation (e.g., `jedis.set("key", "value")`)
2. CommandObjects creates CommandObject with serialized arguments
3. CommandExecutor obtains connection from provider
4. Connection sends command via RedisOutputStream
5. Response read from RedisInputStream
6. Builder deserializes response to Java type
7. Connection returned to pool
8. Result returned to caller

### Cluster Command Execution
1. Command arguments hashed to determine slot
2. ClusterConnectionProvider retrieves connection for slot's node
3. Command executed on target node
4. MOVED/ASK redirections handled automatically
5. Slot cache updated on topology changes
6. Result returned after successful execution

### Multi-Database Failover Flow
1. Command routed to active database
2. Circuit breaker checks database health status
3. If open, fallback to next healthy database
4. Retry logic applies on transient failures
5. Health probes run asynchronously
6. Database transitions to closed state when healthy
7. Active database switches on sustained failures

### Pipeline Execution
1. Commands queued without immediate execution
2. `sync()` triggers batch transmission
3. All commands sent in single network round-trip
4. Responses collected and matched to Response objects
5. Results available via Response.get() after sync

### Transaction Execution
1. MULTI command initiates transaction
2. Commands queued on server side
3. EXEC atomically executes all queued commands
4. Results returned as list
5. DISCARD aborts transaction if needed

### Client-Side Caching Flow
1. Command checked against cache before execution
2. Cache hit returns stored value immediately
3. Cache miss executes command on server
4. Response stored in cache with eviction policy
5. Invalidation messages update/remove cached entries