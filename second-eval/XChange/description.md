# XChange System - High-Level Overview

## System Purpose
XChange is a Java-based cryptocurrency exchange integration framework that provides a unified API for interacting with multiple cryptocurrency exchanges (Binance, Bitfinex, Kraken, OKEx, Coinbase Pro, etc.). It abstracts exchange-specific implementations into a common interface for trading, market data retrieval, and account management.

## Key Components & Responsibilities

### Core Service Layer
- **BaseExchange**: Central exchange abstraction providing lifecycle management (initialization, connection handling) and service access points
- **BaseExchangeService**: Foundation for all exchange-specific services, providing common utilities for order and metadata handling
- **AccountService**: Manages account operations including balance retrieval, deposits, withdrawals, and funding records
- **TradeService**: Handles order placement, cancellation, modification, and trade history retrieval
- **MarketDataService**: Provides real-time and historical market data (tickers, order books, trades, funding rates)

### Exchange-Specific Adapters
- **Adapter Classes** (BinanceAdapters, BitfinexAdapters, KrakenAdapters, etc.): Convert exchange-specific DTOs to standardized XChange domain objects
- **Raw Service Classes**: Direct API communication layers for each exchange (e.g., BitfinexTradeServiceRaw, OkexAccountServiceRaw)
- **Authentication**: Exchange-specific signature generation (BaseParamsDigest implementations) for secure API requests

### Streaming Services
- **NettyStreamingService**: WebSocket-based real-time data streaming using Netty framework
- **StreamingMarketDataService**: Real-time market data subscriptions (order books, trades, tickers)
- **BinanceStreamingMarketDataService**: Exchange-specific streaming implementation with subscription management

### Data Transfer Objects (DTOs)
- **Market Data DTOs**: Order books, tickers, trades, candlestick data
- **Trade DTOs**: Orders (limit, market, stop), user trades, positions
- **Account DTOs**: Balances, wallets, funding records, fees

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core programming language
- **JAX-RS (Jakarta)**: RESTful API client implementation (@POST, @GET, @Path annotations)
- **Netty**: Asynchronous event-driven network framework for WebSocket connections
- **RxJava 3**: Reactive programming for streaming data (Observable, Completable, Single)
- **Jackson**: JSON serialization/deserialization
- **SLF4J**: Logging facade

### Key Libraries
- **Rescu (si.mazi.rescu)**: REST client framework with signature support
- **Lombok**: Boilerplate code reduction (@Getter, @Setter, @Builder)
- **Resilience4j**: Rate limiting and resilience patterns
- **Bouncy Castle**: Cryptographic operations for API authentication
- **Web3j**: Ethereum integration (for DEX support like IDEX)

## Architecture

### Layered Architecture
```
┌─────────────────────────────────────┐
│   Client Application Layer          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   XChange Unified API                │
│   (Exchange, AccountService,         │
│    TradeService, MarketDataService)  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Adapter Layer                      │
│   (Exchange-specific adapters)       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Raw Service Layer                  │
│   (Direct API communication)         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Transport Layer                    │
│   (REST: Rescu, WebSocket: Netty)   │
└─────────────────────────────────────┘
```

### Design Patterns
- **Adapter Pattern**: Converts exchange-specific data to common domain models
- **Factory Pattern**: Exchange instantiation and service creation
- **Builder Pattern**: Complex object construction (Orders, DTOs)
- **Observer Pattern**: Reactive streams for real-time data (RxJava Observables)
- **Strategy Pattern**: Exchange-specific authentication and rate limiting

## Data Flow

### REST API Flow (Trading/Account Operations)
1. Client invokes method on service interface (e.g., `TradeService.placeLimitOrder()`)
2. Service delegates to exchange-specific raw service
3. Raw service constructs authenticated request with signature
4. Rescu framework executes HTTP request with rate limiting
5. Exchange returns JSON response
6. Jackson deserializes to exchange-specific DTO
7. Adapter converts DTO to standardized XChange domain object
8. Result returned to client

### WebSocket Streaming Flow (Market Data)
1. Client subscribes to instrument via `StreamingMarketDataService`
2. NettyStreamingService establishes WebSocket connection
3. Subscription message sent to exchange
4. Exchange streams real-time updates
5. Netty handlers parse incoming messages
6. Exchange-specific adapters convert to domain objects
7. RxJava Observable emits updates to subscribers
8. Client receives real-time data via reactive stream

### Initialization Flow
1. `BaseExchange.remoteInit()` fetches exchange metadata (instruments, fees, limits)
2. Metadata stored in `ExchangeMetaData` (currency pairs, trading rules, precision)
3. Services initialized with exchange configuration
4. Rate limiters configured per exchange specifications
5. Authentication credentials loaded from `ExchangeSpecification`

### Error Handling
- Exchange-specific exceptions wrapped in standardized exceptions (`ExchangeException`, `FundsExceededException`)
- Rate limit enforcement via Resilience4j decorators
- Automatic reconnection logic for WebSocket disconnections
- Validation of order parameters against exchange metadata