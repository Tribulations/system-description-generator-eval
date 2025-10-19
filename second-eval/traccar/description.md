# Traccar System Overview

## System Purpose
Traccar is a GPS tracking server system that receives, processes, stores, and forwards location data from various GPS tracking devices. It provides real-time tracking, event management, notifications, and reporting capabilities for fleet management and asset tracking.

## Key Components & Responsibilities

### Protocol Layer
- **BaseProtocol & Protocol Decoders**: Handles communication with 50+ different GPS device protocols (Teltonika, GT06, Suntech, Huabao, etc.)
- **BaseProtocolDecoder/Encoder**: Decodes binary/text messages from devices and encodes commands back to devices
- **BaseHttpProtocolDecoder**: Processes HTTP-based device protocols (Sigfox, Globalstar, Osmand)
- **BasePipelineFactory**: Configures Netty channel pipelines for each protocol

### Session Management
- **ConnectionManager**: Manages active device connections and tracks online/offline status
- **DeviceSession**: Maintains session state for connected devices
- **CacheManager**: Caches devices, users, groups, geofences, and other entities for fast access

### Data Processing Pipeline
- **ProcessingHandler**: Orchestrates position data through handler chain
- **FilterHandler**: Filters invalid positions based on accuracy, duplicates, and time constraints
- **GeolocationHandler**: Resolves location from cell tower/WiFi data when GPS unavailable
- **GeocoderHandler**: Reverse geocodes coordinates to addresses
- **ComputedAttributesHandler**: Calculates custom attributes using JEXL expressions
- **Event Handlers**: Detects and generates events (geofence, overspeed, motion, maintenance, etc.)
- **DatabaseHandler**: Persists positions and events to storage

### Storage Layer
- **DatabaseStorage**: Primary storage implementation using JDBC with HikariCP connection pooling
- **QueryBuilder**: Constructs SQL queries dynamically
- **Storage Interface**: Abstraction for CRUD operations on domain models

### API & Web Layer
- **WebServer**: Jetty-based HTTP server hosting REST API and WebSocket endpoints
- **Resource Classes**: JAX-RS REST endpoints (DeviceResource, UserResource, PositionResource, etc.)
- **AsyncSocket**: WebSocket implementation for real-time updates to web clients
- **SecurityRequestFilter**: Handles authentication and authorization

### Notification System
- **NotificationManager**: Coordinates event notifications to users
- **NotificatorManager**: Manages multiple notification channels
- **Notificators**: Implementations for email, SMS, Firebase, Telegram, web push, etc.
- **TextTemplateFormatter**: Formats notification messages using Velocity templates

### Forwarding & Integration
- **PositionForwarder**: Forwards position data to external systems (HTTP, MQTT, Kafka, Redis, AMQP)
- **EventForwarder**: Forwards events to external systems
- **CommandsManager**: Manages command queue and delivery to devices

### Reporting
- **Report Providers**: Generate various reports (trips, stops, summary, events, routes, combined)
- **ReportUtils**: Common utilities for report generation
- **Export Providers**: Export data in CSV, KML, GPX formats

### Background Tasks
- **ScheduleManager**: Manages scheduled tasks
- **TaskReports**: Generates and emails scheduled reports
- **TaskDeviceInactivityCheck**: Monitors device inactivity
- **TaskExpirations**: Handles user/device expiration notifications

## Core Technologies & Dependencies

### Framework & Server
- **Netty**: Asynchronous event-driven network framework for protocol handling
- **Jetty**: Embedded web server and servlet container
- **Google Guice**: Dependency injection framework

### Data & Persistence
- **JDBC**: Database connectivity with HikariCP connection pooling
- **Liquibase**: Database schema migration
- **Jackson**: JSON serialization/deserialization

### API & Web
- **JAX-RS (Jersey)**: RESTful web services
- **WebSocket**: Real-time bidirectional communication
- **Apache Velocity**: Template engine for notifications and reports

### Messaging & Integration
- **MQTT, Kafka, AMQP, Redis**: Message broker integrations
- **Firebase**: Push notifications
- **JavaMail**: Email notifications

### Utilities
- **Apache Commons**: Various utility libraries
- **JEXL**: Expression language for computed attributes
- **iCal4j**: Calendar/scheduling support
- **Protocol Buffers**: Binary serialization for specific protocols

## Architecture

Traccar follows a **layered architecture** with clear separation of concerns:

1. **Network Layer**: Netty-based protocol handlers receive device data
2. **Session Layer**: Manages device connections and authentication
3. **Processing Layer**: Chain of handlers processes and enriches position data
4. **Business Logic Layer**: Event detection, notifications, command management
5. **Persistence Layer**: Database storage with caching
6. **API Layer**: REST and WebSocket interfaces for client applications
7. **Integration Layer**: Forwards data to external systems

The system uses **dependency injection** (Guice) throughout, with singleton services managing shared state and resources.

## Data Flow

### Inbound Position Data Flow
1. Device connects via specific protocol (TCP/UDP/HTTP)
2. Protocol decoder parses binary/text message into Position object
3. DeviceSession validates and associates device
4. ProcessingHandler routes through handler chain:
   - FilterHandler validates position quality
   - GeolocationHandler resolves location if needed
   - GeocoderHandler adds address
   - ComputedAttributesHandler calculates custom fields
   - Event handlers detect events (geofence entry/exit, overspeed, etc.)
   - DatabaseHandler persists to storage
5. ConnectionManager broadcasts updates to WebSocket clients
6. PositionForwarder sends to external systems if configured
7. NotificationManager triggers alerts based on events

### Outbound Command Flow
1. User submits command via REST API
2. CommandsManager queues command
3. Command delivered to device via protocol encoder when device connects
4. Acknowledgment processed and stored

### Report Generation Flow
1. User requests report via API
2. Report provider queries storage for relevant data
3. Data aggregated and formatted (Excel/PDF)
4. Report returned or emailed to user

### Real-time Updates Flow
1. WebSocket client connects and authenticates
2. AsyncSocket registers client for device updates
3. Position updates broadcast to subscribed clients
4. Events and device status changes pushed in real-time