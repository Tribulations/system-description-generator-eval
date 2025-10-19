
# RuneLite System Overview

## System Purpose
RuneLite is a third-party client for Old School RuneScape (OSRS) that enhances the vanilla game client with additional features, overlays, and quality-of-life improvements through a plugin-based architecture.

## Key Components & Responsibilities

### Core Framework
- **Client**: Central API interface extending `OAuthApi` and `GameEngine`, providing access to game state, player data, world information, and rendering capabilities
- **RuneLite**: Main entry point handling application initialization, dependency injection via Guice, and system configuration
- **ClientUI**: Manages the application window, UI components, navigation, and user interface state
- **Hooks/Callbacks**: Bridge between the game client and plugin system, intercepting game events and rendering calls

### Plugin System
- **Plugin**: Base class for all plugins, integrates with Guice for dependency injection
- **PluginManager**: Handles plugin lifecycle (loading, starting, stopping), dependency resolution using graph-based ordering, and scheduled task management
- **ExternalPluginManager**: Manages third-party plugins from external sources, handles installation, updates, and verification

### UI & Overlay System
- **Overlay**: Base class for rendering custom overlays on the game canvas, supports positioning and priority management
- **OverlayManager**: Coordinates overlay rendering across different layers
- **Layout/ClientUI**: Custom layout manager for UI components, handles window management and component positioning

### Major Plugins
- **ClueScrollPlugin**: Assists with treasure trail clues, provides hints and location information
- **LootTrackerPlugin**: Tracks and records loot from various activities
- **GrandExchangePlugin**: Enhances Grand Exchange interface with price tracking and history
- **GroundItemsPlugin**: Highlights and filters ground items based on value and configuration
- **BankPlugin/BankTagsPlugin**: Adds search, tagging, and organization features to the bank interface
- **RaidsPlugin**: Provides raid-specific overlays and scouting information
- **PartyPlugin**: Enables party/group features with real-time synchronization
- **MusicPlugin**: Enhances music player with custom controls and volume management
- **WorldHopperPlugin**: Facilitates world switching with ping information and favorites

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core programming language
- **Guice**: Dependency injection framework
- **LWJGL**: OpenGL bindings for GPU rendering
- **OpenCL**: GPU compute for advanced rendering features
- **OkHttp**: HTTP client for API communication
- **Gson**: JSON serialization/deserialization
- **Logback/SLF4J**: Logging framework
- **Lombok**: Code generation for boilerplate reduction

### UI Technologies
- **Swing**: Primary UI framework
- **FlatLaf**: Modern look-and-feel for Swing components
- **AWT**: Graphics and event handling

### External Services
- **RuneLite HTTP API**: Item prices, world information, and player data
- **WebSocket**: Real-time party/group communication
- **Discord**: Rich presence integration

## Architecture

### Layered Architecture
1. **Game Client Layer**: Modified OSRS client with injected hooks
2. **API Layer**: Abstraction over game client (`net.runelite.api`)
3. **Core Services Layer**: Event bus, configuration, callbacks, managers
4. **Plugin Layer**: Modular features as independent plugins
5. **UI Layer**: Overlays, panels, and interface components

### Event-Driven Design
- **EventBus**: Central event distribution system using Subscribe annotations
- **ClientThread**: Ensures game state modifications occur on the correct thread
- **Callbacks/Hooks**: Intercepts game events (rendering, ticks, state changes)

### Plugin Architecture
- Plugins are self-contained modules with their own configuration
- Dependency injection provides access to core services
- Plugins can depend on other plugins (resolved via dependency graph)
- Lifecycle managed through `startUp()` and `shutDown()` methods

## Data Flow

### Game Event Flow
1. Game client triggers event (tick, render, state change)
2. Hooks/Callbacks intercept and wrap event
3. EventBus distributes to subscribed plugins
4. Plugins process event and update state
5. Overlays render based on updated state

### User Input Flow
1. User interacts with UI or game canvas
2. MouseManager/KeyManager captures input
3. Input routed to appropriate handlers (plugins, overlays, UI components)
4. Handlers process input and trigger actions
5. Actions may modify game state or UI state

### Configuration Flow
1. User modifies settings in plugin configuration panel
2. ConfigManager persists changes to disk
3. ConfigChanged event published to EventBus
4. Relevant plugins receive event and update behavior
5. Changes reflected in overlays and game interactions

### Data Synchronization Flow
1. Game state changes detected via varbit/varp monitoring
2. ItemManager/NPCManager cache and provide game data
3. Plugins query managers for current state
4. External data fetched from HTTP API as needed
5. Party/group data synchronized via WebSocket

### Rendering Pipeline
1. Game renders base scene to buffer
2. DrawCallbacks intercepts render calls
3. GPU plugin (if enabled) processes via OpenGL/OpenCL
4. OverlayManager renders overlays in layers (background, game, widgets, tooltips)
5. Final composite presented to user