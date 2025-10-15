# OctoUML System Overview

## 1. System Purpose
OctoUML is a collaborative UML diagram editor built with JavaFX. It enables users to create, edit, and share UML class diagrams and sequence diagrams with support for real-time collaboration, sketch recognition, and version control integration.

## 2. Key Components & Responsibilities

### Model Layer (`model` package)
- **Graph**: Central data structure managing collections of nodes, edges, and sketches
- **AbstractNode/Node**: Base classes for diagram elements (ClassNode, PackageNode, SequenceObject, PictureNode)
- **AbstractEdge/Edge**: Relationship representations (AssociationEdge, InheritanceEdge, CompositionEdge, AggregationEdge, MessageEdge)
- **Sketch**: Freehand drawing support with stroke and path data
- **GraphElement**: Common interface for all diagram elements with positioning and selection capabilities

### View Layer (`view` package)
- **AbstractNodeView**: Visual representation base for nodes with property change listening
- **Concrete Node Views**: ClassNodeView, PackageNodeView, SequenceObjectView, PictureNodeView
- **AbstractEdgeView**: Visual representation base for edges with line rendering
- **Concrete Edge Views**: AssociationEdgeView, InheritanceEdgeView, CompositionEdgeView, AggregationEdgeView, MessageEdgeView

### Controller Layer (`controller` package)
- **AbstractDiagramController**: Base controller with grid drawing, snapshot generation, and common diagram operations
- **ClassDiagramController**: Manages class diagram-specific interactions
- **SequenceDiagramController**: Handles sequence diagram operations including message ordering
- **TabController**: Manages multiple diagram tabs and application lifecycle
- **NodeController**: Handles node creation, selection, and editing
- **EdgeController**: Manages edge creation and connection logic
- **CreateNodeController**: Coordinates node instantiation workflow
- **SelectController**: Implements selection and multi-select behavior
- **SketchController**: Manages freehand drawing mode
- **RecognizeController**: Integrates sketch recognition to convert drawings into UML elements
- **CopyPasteController**: Implements clipboard operations for diagram elements
- **GraphController**: Manages graph-level operations
- **VoiceController/VoiceTask**: Provides voice command functionality

### Collaboration (`controller` package)
- **ServerController**: Hosts collaborative sessions, broadcasts changes to connected clients
- **ClientController**: Connects to remote sessions, synchronizes local changes with server

### Dialog Controllers (`controller.dialog` package)
- **NodeEditDialogController**: Node property editing interface
- **EdgeEditDialogController**: Edge property editing interface
- **MessageEditDialogController**: Message edge-specific editing
- **GithubLoginDialogController**: GitHub authentication
- **GithubRepoDialogController**: Repository selection and configuration

## 3. Core Technologies & Dependencies

### Primary Framework
- **JavaFX**: UI framework for rendering, event handling, and scene graph management

### Networking
- **KryoNet**: Client-server networking for real-time collaboration with Kryo serialization

### Recognition
- **PaleoSketch**: Sketch recognition library for converting hand-drawn shapes into UML elements

### Voice Recognition
- **CMU Sphinx**: Speech recognition for voice commands

### Version Control
- **JGit**: Git integration for diagram versioning and GitHub synchronization

### UI Components
- **ControlsFX**: Enhanced JavaFX controls for notifications and dialogs

### Utilities
- **Java ImageIO**: Image export functionality
- **Java Beans**: Property change support for observer pattern implementation

## 4. Architecture

OctoUML follows a **Model-View-Controller (MVC) architecture** with observer pattern integration:

- **Model**: Pure data classes implementing Serializable for persistence and network transmission. Models use PropertyChangeSupport to notify observers of state changes.

- **View**: JavaFX Group-based visual components that observe model changes through PropertyChangeListener. Views automatically update when model properties change.

- **Controller**: Event handlers and business logic coordinators. Controllers manipulate models through command pattern implementations and manage view creation/destruction.

**Key Patterns**:
- **Observer Pattern**: Models notify views of changes via PropertyChangeListener
- **Command Pattern**: User actions encapsulated as commands (implied by command package imports)
- **Factory Pattern**: Node and edge view creation based on model types
- **Serialization**: All model classes implement Serializable for persistence and network transfer

## 5. Data Flow

### User Interaction Flow
1. User interacts with JavaFX UI (mouse/touch/voice events)
2. Controller receives event and validates action
3. Controller creates/executes command object
4. Command modifies model state
5. Model fires PropertyChangeEvent
6. View receives notification and updates visual representation
7. If collaborative mode active, change broadcasts to ServerController/ClientController

### Collaborative Session Flow
1. ServerController hosts session and listens for connections
2. ClientController connects and registers with server
3. Local model changes trigger PropertyChangeEvents
4. Controller serializes change and sends via KryoNet
5. Remote ServerController receives change and applies to local model
6. Server broadcasts change to all connected clients
7. Clients deserialize and apply change to their local models
8. Views update automatically via observer pattern

### Sketch Recognition Flow
1. SketchController captures mouse/touch input as stroke data
2. Stroke data stored in Sketch model object
3. RecognizeController invokes PaleoSketchRecognizer
4. Recognizer analyzes stroke patterns and returns shape classification
5. Controller converts recognized shape to appropriate UML element (ClassNode, Edge, etc.)
6. New element added to Graph model
7. Corresponding view created and rendered

### Persistence Flow
1. TabController triggers save operation
2. PersistenceManager serializes Graph model to XML/binary format
3. File written to disk or pushed to Git repository via JGit
4. Load operation deserializes file back to Graph model
5. Controllers recreate views from restored model state
