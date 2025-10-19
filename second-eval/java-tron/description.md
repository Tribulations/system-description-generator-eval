# Java-TRON System Overview

## System Purpose
Java-TRON is a blockchain implementation that provides a complete cryptocurrency platform with smart contract execution capabilities, consensus mechanisms, and decentralized resource management. The system handles transaction processing, block validation, account management, and virtual machine execution for smart contracts.

## Key Components & Responsibilities

### Core Layer
- **Wallet**: Central component managing blockchain operations including transaction creation, account queries, market operations, and cryptographic functions (shielded transactions, key generation)
- **Manager**: Database and blockchain state coordinator handling block processing, transaction validation, event triggering, and maintaining consensus state
- **ChainBaseManager**: Provides unified access to all storage components and manages the blockchain's persistent state

### Storage Layer
- **DynamicPropertiesStore**: Manages blockchain configuration parameters including energy pricing, resource limits, maintenance schedules, and protocol upgrade flags
- **Specialized Stores**: Dedicated storage for accounts, contracts, transactions, witnesses, proposals, exchanges, and market data

### API Layer
- **DatabaseApi**: Primary gRPC service exposing blockchain query and transaction submission endpoints
- **WalletApi**: Main wallet operations interface for account management and transaction creation
- **WalletSolidityApi**: Read-only interface for querying solidified (confirmed) blockchain state
- **WalletExtensionApi**: Extended functionality for advanced features like shielded transactions
- **MonitorApi**: System monitoring and metrics collection interface

### Execution Layer
- **Program**: Virtual machine program executor managing smart contract execution state, memory, stack operations, and energy consumption
- **PrecompiledContract**: Native contract implementations for cryptographic operations (signature verification, hashing, pairing checks) and system functions

### Service Layer
- **RpcApiService**: Orchestrates API request handling and response formatting
- **RateLimiterServlet**: HTTP request rate limiting and traffic management
- **MetricsApiService**: Performance monitoring and metrics aggregation

### Data Model
- **AccountCapsule**: Encapsulates account state including balances, frozen assets, delegated resources, voting power, and resource usage tracking

## Core Technologies & Dependencies

### Blockchain Framework
- **Protocol Buffers**: Data serialization for all blockchain structures
- **gRPC**: Remote procedure call framework for API services
- **Netty**: High-performance network communication

### Storage & State Management
- **Custom Key-Value Store**: Chainbase implementation with snapshot and rollback capabilities
- **LevelDB/RocksDB**: Underlying persistent storage engines

### Cryptography
- **Bouncy Castle**: Cryptographic primitives and signature schemes
- **zkSNARK Libraries**: Zero-knowledge proof support via JLibrustzcash
- **Blake2b, SHA-256**: Hashing algorithms

### Smart Contract Execution
- **Custom EVM Implementation**: Ethereum-compatible virtual machine with TRON-specific extensions
- **Energy Metering**: Resource consumption tracking and limiting

### Concurrency & Performance
- **Java Executors**: Thread pool management for parallel processing
- **Guava Cache**: In-memory caching for frequently accessed data
- **Prometheus**: Metrics collection and monitoring

## Architecture

The system follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         API Layer (gRPC Services)       │
│  DatabaseApi, WalletApi, MonitorApi     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Business Logic Layer               │
│  Wallet, Manager, Consensus             │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Execution Layer                    │
│  VM (Program), Precompiled Contracts    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Storage Layer                      │
│  ChainBaseManager, Specialized Stores   │
└─────────────────────────────────────────┘
```

**Key Architectural Patterns:**
- **Capsule Pattern**: Wraps Protocol Buffer messages with business logic (AccountCapsule, BlockCapsule, TransactionCapsule)
- **Repository Pattern**: Abstracts storage access through store interfaces
- **Factory Pattern**: Creates actuators, contracts, and invocation contexts
- **Observer Pattern**: Event-driven triggers for logging and monitoring

## Data Flow

### Transaction Processing Flow
1. **Submission**: Client submits transaction via gRPC API (WalletApi/DatabaseApi)
2. **Validation**: Manager validates transaction signature, expiration, and resource availability
3. **Execution**: 
   - For transfers: Direct balance updates via actuators
   - For smart contracts: Program executes bytecode in VM with energy metering
4. **State Update**: Changes committed to ChainBaseManager stores
5. **Block Production**: Witness nodes package transactions into blocks
6. **Consensus**: Block validation and solidification through DPoS consensus
7. **Finalization**: Solidified blocks trigger event notifications and metrics updates

### Query Flow
1. **Request**: Client queries via API (read-only operations use WalletSolidityApi)
2. **Store Access**: ChainBaseManager routes to appropriate specialized store
3. **Data Retrieval**: Store fetches from cache or persistent storage
4. **Serialization**: Data wrapped in Protocol Buffer messages
5. **Response**: gRPC returns formatted response to client

### Resource Management Flow
- **Energy/Bandwidth Calculation**: DynamicPropertiesStore provides pricing and limits
- **Consumption Tracking**: AccountCapsule records usage timestamps and amounts
- **Regeneration**: Time-based resource recovery using window-based algorithms
- **Delegation**: Separate tracking for owned vs. delegated resources with FreezeV2 mechanism

### Smart Contract Execution Flow
1. **Contract Call**: TriggerSmartContract transaction received
2. **Context Creation**: Program initialized with caller address, contract address, input data
3. **Bytecode Execution**: VM interprets opcodes, manages stack/memory, calls precompiled contracts
4. **State Changes**: Repository tracks storage modifications
5. **Energy Accounting**: Continuous energy consumption monitoring with overflow protection
6. **Result Capture**: Return data, logs, and internal transactions recorded in ProgramResult
7. **Commit/Revert**: State changes applied or rolled back based on execution success