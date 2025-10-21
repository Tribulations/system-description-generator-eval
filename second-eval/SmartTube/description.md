# SmartTube System Overview

## System Purpose
SmartTube is an Android TV application that provides an enhanced YouTube viewing experience with advanced playback controls, customizable UI, and extended media management capabilities. The system integrates ExoPlayer for media playback and uses the Leanback library for Android TV-optimized user interfaces.

## Key Components & Responsibilities

### Presentation Layer
- **BrowsePresenter**: Manages the main browsing interface, handles section navigation, video group display, and user account state synchronization
- **PlaybackPresenter**: Controls video playback lifecycle, manages player state, and coordinates between UI and playback engine
- **SearchPresenter**: Handles search functionality and search result presentation
- **BasePresenter**: Provides common presenter functionality including view lifecycle management and context handling

### View Layer
- **BrowseView/BrowseFragment**: Main navigation interface displaying video sections and categories
- **PlaybackView/PlaybackFragment**: Video player interface with custom controls and overlays
- **SeekModePlaybackFragment**: Extended playback fragment with advanced seeking capabilities
- **ViewManager**: Coordinates view lifecycle and navigation between different screens

### Media & Playback
- **ExoPlayerController/PlayerController**: Abstracts ExoPlayer operations and provides playback control interface
- **VideoPlayerGlue**: Bridges Leanback PlayerAdapter with ExoPlayer for TV-optimized playback controls
- **FormatItem/MediaTrack**: Represents video/audio format selections and quality options
- **SubtitleManager**: Manages subtitle rendering and styling
- **RestoreTrackSelector**: Persists and restores user track selections across sessions

### Data Management
- **Video/VideoGroup**: Core data models representing video content and collections
- **BrowseSection**: Represents navigable content sections (Home, Subscriptions, History, etc.)
- **PlayerData/MainUIData/SearchData**: Persistent user preferences and settings
- **VideoStateService**: Tracks and persists video playback positions and states

### UI Components
- **ViewHolder**: Leanback widget for rendering list items with custom layouts
- **VideoCardPresenter**: Displays video thumbnails and metadata in grid/list views
- **CustomListRowPresenter**: Custom row presenter for enhanced list rendering
- **ProgressBarManager**: Manages loading indicators across the application

## Core Technologies & Dependencies

### Primary Frameworks
- **ExoPlayer 2.x**: Media playback engine with adaptive streaming support
- **AndroidX Leanback**: TV-optimized UI components and navigation patterns
- **AndroidX Fragment**: Modern fragment management and lifecycle handling
- **RxJava 2.x**: Reactive programming for asynchronous operations

### Media Services
- **YouTube API (via MediaServiceInterfaces)**: Content retrieval and metadata access
- **MediaSessionCompat**: Media session management for external control and notifications

### Supporting Libraries
- **Glide**: Image loading and caching
- **Gson**: JSON serialization/deserialization
- **SharedPreferences**: Local data persistence

## Architecture

The system follows a **Model-View-Presenter (MVP)** architecture with reactive data flow:

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                  │
│  (Presenters: Browse, Playback, Search, etc.)   │
└──────────────┬──────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────┐
│                View Layer                        │
│  (Fragments, Activities, Custom Views)           │
└──────────────┬──────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────┐
│            Service/Manager Layer                 │
│  (MediaServiceManager, AppDataSourceManager)    │
└──────────────┬──────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────────┐
│          Data/Playback Layer                     │
│  (ExoPlayer, Data Models, Preferences)           │
└─────────────────────────────────────────────────┘
```

## Data Flow

### Content Browsing Flow
1. **BrowsePresenter** requests content from **MediaServiceManager**
2. **MediaServiceManager** fetches data via **YouTube API** through reactive observables
3. Data transforms into **VideoGroup** and **Video** models
4. **BrowseView** receives updates and renders content via **VideoCardPresenter**
5. User selections trigger navigation through **ViewManager**

### Playback Flow
1. User selects video → **BrowsePresenter** initiates playback via **PlaybackPresenter**
2. **PlaybackPresenter** configures **ExoPlayerController** with video source
3. **ExoPlayerController** initializes **SimpleExoPlayer** with format selectors
4. **VideoPlayerGlue** binds player to **PlaybackFragment** UI controls
5. **PlayerEventListener** monitors playback events and updates **VideoStateService**
6. **SubtitleManager** and **DebugInfoManager** provide auxiliary playback features

### Settings Persistence Flow
1. User modifies settings in UI → Presenter updates corresponding **Data** class (PlayerData, MainUIData)
2. **Data** classes serialize changes to **SharedPreferences**
3. **ProfileChangeListener** notifies dependent components of configuration changes
4. Components reload settings and apply new configurations

### Track Selection Flow
1. User requests quality/subtitle change → **PlaybackPresenter** invokes **RestoreTrackSelector**
2. **RestoreTrackSelector** queries available **TrackGroup** options from **ExoPlayer**
3. User selection converts to **FormatItem** and persists in **PlayerData**
4. **DefaultTrackSelector** applies **SelectionOverride** to active playback
5. **ExoPlayer** switches tracks seamlessly during playback