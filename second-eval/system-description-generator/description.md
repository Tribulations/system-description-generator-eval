# SDG System - High-Level Summary

## 1. System Purpose
The SDG system is a **Java software analysis and visualization tool** that parses Java codebases, extracts structural and behavioral information, stores it in a Neo4j graph database, and generates PlantUML diagrams using LLM services (Claude/Gemini) to visualize system architecture and relationships.

## 2. Key Components & Responsibilities

### View Layer (`com.sdg.view`)
- **MainView**: Swing-based GUI (JFrame) providing user interface with input fields, process button, output area, loading indicators, and tabbed diagram display.

### Controller Layer (`com.sdg.controller`)
- **InputController**: Orchestrates user interactions, coordinates between view and services, manages file selection, and handles asynchronous processing workflows using RxJava.

### Model Layer (`com.sdg.model`)
- **InputHandler**: Processes input sources (local directories or Git repositories), validates Java files, and prepares them for analysis.

### AST Analysis (`com.sdg.ast`)
- **JavaFileParser**: Parses Java source files into Abstract Syntax Trees using JavaParser.
- **ASTAnalyzer**: Extracts structural information (classes, methods, fields) from ASTs.
- **MethodCallAnalyzer**: Analyzes method invocations and resolves call relationships using JavaParser's symbol solver.
- **MethodAnalysisHelper**: Provides filtering and helper utilities for method analysis with configurable filtering percentages.

### Graph Database (`com.sdg.graph`)
- **GraphDatabaseOperations**: Manages Neo4j driver connections, batch transactions, and session lifecycle.
- **KnowledgeGraphService**: High-level service coordinating AST analysis and graph database population using reactive streams.
- **SchemaInitializer**: Sets up Neo4j database schema with constraints and indexes.
- **GraphDataToJsonConverter**: Exports graph data to JSON format for external consumption.

### Graph Model (`com.sdg.graph.model`)
- **SystemStructure**: Root container for the entire system representation.
- **ClassNode**: Represents Java classes with imports, extended classes, and implemented interfaces.
- **MethodNode**: Represents methods with signatures and metadata.
- **MethodCallNode**: Represents method invocation relationships.
- **ClassFieldNode**: Represents class fields.
- **ControlFlowNode**: Represents control flow structures (if/for statements).

### LLM Integration (`com.sdg.llm`)
- **LLMService**: Orchestrates LLM API calls with retry logic and file-based caching.
- **ClaudeApiClient**: HTTP client for Anthropic's Claude API.
- **GeminiApiClient**: HTTP client for Google's Gemini API.
- **BaseClient**: Shared HTTP client infrastructure with timeout configuration.
- **PythonClient**: Alternative client for Python-based LLM services.

### Diagram Generation (`com.sdg.diagrams`)
- **DiagramFetcher**: Retrieves PlantUML diagram definitions from LLM services.
- **DiagramTabManager**: Manages multiple diagram tabs in the UI (JTabbedPane).
- **DiagramTab**: Individual diagram container with lazy rendering.
- **ScalableImagePanel**: Custom JPanel for rendering and scaling PlantUML-generated images.
- **PlantUMLValidator**: Validates PlantUML syntax before rendering.
- **PlantUMLDiagramExtractor**: Extracts PlantUML code blocks from LLM responses.

## 3. Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core programming language (Swing for GUI)
- **Neo4j**: Graph database for storing code structure and relationships
- **JavaParser**: AST parsing and symbol resolution
- **RxJava 3**: Reactive programming for asynchronous operations
- **PlantUML**: Diagram generation from textual descriptions

### Key Libraries
- **Jackson**: JSON serialization/deserialization
- **JGit**: Git repository cloning and operations
- **SLF4J**: Logging facade
- **Java HTTP Client**: HTTP communication with LLM APIs

### External Services
- **Anthropic Claude API**: LLM for diagram generation
- **Google Gemini API**: Alternative LLM provider

## 4. Architecture

The system follows a **layered MVC architecture** with reactive extensions:

```
Presentation Layer (Swing GUI)
         ↓
Controller Layer (Event Handling & Orchestration)
         ↓
Service Layer (Knowledge Graph, LLM, Diagram Services)
         ↓
Data Access Layer (Neo4j Operations, AST Analysis)
         ↓
External Systems (Neo4j Database, LLM APIs)
```

**Key Architectural Patterns:**
- **MVC Pattern**: Separation of view, controller, and model concerns
- **Reactive Streams**: RxJava Observables/Singles for asynchronous processing
- **Repository Pattern**: GraphDatabaseOperations abstracts database access
- **Service Layer**: Business logic encapsulation in dedicated services
- **Batch Processing**: Transaction batching for efficient graph database writes

## 5. Data Flow

### Analysis Pipeline
1. **Input Acquisition**: User selects directory/Git URL → InputHandler validates and collects Java files
2. **AST Parsing**: JavaFileParser converts source files to CompilationUnits
3. **Structure Extraction**: ASTAnalyzer traverses ASTs extracting classes, methods, fields, control flow
4. **Relationship Analysis**: MethodCallAnalyzer resolves method call relationships using symbol solver
5. **Graph Storage**: GraphDatabaseOperations writes nodes and relationships to Neo4j in batches
6. **JSON Export**: GraphDataToJsonConverter queries Neo4j and serializes to JSON

### Diagram Generation Pipeline
1. **Graph Query**: System retrieves stored structure from Neo4j
2. **LLM Request**: DiagramFetcher sends structure to Claude/Gemini with PlantUML generation prompt
3. **Response Processing**: PlantUMLDiagramExtractor parses LLM response for diagram code
4. **Validation**: PlantUMLValidator checks syntax correctness
5. **Rendering**: PlantUML library converts text to BufferedImage
6. **Display**: DiagramTabManager creates tabs with ScalableImagePanel for user viewing

### Reactive Flow Control
- **Schedulers.io()**: File I/O and network operations
- **SwingUtilities.invokeLater()**: UI updates on Event Dispatch Thread
- **CompositeDisposable**: Manages subscription lifecycle in controller
- **CompletableFuture**: LLM API calls with timeout handling
