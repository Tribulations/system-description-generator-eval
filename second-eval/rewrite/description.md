# OpenRewrite System - High-Level Summary

## 1. System Purpose

OpenRewrite is a Java-based code transformation and refactoring framework that parses, analyzes, and modifies source code across multiple programming languages and configuration formats. The system enables automated code migrations, style enforcement, and structural transformations through a recipe-based architecture.

## 2. Key Components & Responsibilities

### Builder Class (org.openrewrite.properties.Builder)
- **Primary Role:** Factory pattern implementation for constructing parser and template objects
- **Responsibilities:**
  - Creates parser instances for multiple formats (Maven, Properties, Gradle, XML, JSON, YAML, TOML, Proto, HCL, Kotlin, Groovy, PlainText)
  - Builds template objects for code generation (JavaTemplate, GroovyTemplate, HclTemplate, KotlinTemplate)
  - Constructs padded tree elements (JRightPadded, JLeftPadded, JsonRightPadded, TomlRightPadded, ProtoRightPadded, HclRightPadded)
  - Manages compilation settings and import configurations
  - Implements Cloneable for builder pattern reusability

### Recipe Class (org.openrewrite.Recipe)
- **Primary Role:** Abstract base class for defining code transformation rules
- **Responsibilities:**
  - Defines transformation logic through visitor pattern implementation
  - Validates recipe configuration and parameters
  - Manages recipe metadata (name, display name, estimated effort)
  - Supports recipe composition through child recipe lists
  - Provides visitor delegation for tree traversal and modification

## 3. Core Technologies & Dependencies

### Language Support
- **Java:** Primary implementation language with JavaParser, JavaTemplate, and Java AST manipulation
- **Kotlin:** Full parsing and transformation support via JetBrains Kotlin compiler integration
- **Groovy:** Codehaus Groovy compiler integration for parsing and transformation
- **Configuration Formats:** XML, JSON, YAML, TOML, Properties, HCL, Protocol Buffers

### Key Dependencies
- **Parsing:** ANTLR4 for grammar-based parsing, Sun Tools Javac for Java compilation
- **Kotlin Integration:** JetBrains Kotlin compiler (FIR - Frontend Intermediate Representation)
- **Groovy Integration:** Codehaus Groovy compiler and control flow analysis
- **Metrics:** Micrometer for instrumentation and performance monitoring
- **Serialization:** Jackson for JSON processing and configuration
- **Build Tools:** Maven and Gradle parser integration
- **Utilities:** Lombok for boilerplate reduction, SnakeYAML for YAML processing

## 4. Architecture

### Layered Architecture Pattern
1. **Parser Layer:** Language-specific parsers convert source text to Lossless Semantic Trees (LST)
2. **Tree Model Layer:** Immutable AST representations with full formatting preservation
3. **Visitor Layer:** Tree traversal and transformation logic using visitor pattern
4. **Recipe Layer:** High-level transformation definitions composing visitors
5. **Execution Layer:** Recipe orchestration with context management and error handling

### Design Patterns
- **Builder Pattern:** Fluent API for parser and template construction
- **Visitor Pattern:** Tree traversal and modification without altering tree structure
- **Template Method:** Recipe base class defines transformation workflow
- **Factory Pattern:** Parser creation abstracted through builder methods
- **Immutable Data Structures:** All tree nodes are immutable with copy-on-write semantics

## 5. Data Flow

### Parsing Flow
1. **Input:** Source code as InputStream or Path with encoding detection
2. **Lexical Analysis:** Language-specific lexer tokenizes input
3. **Syntax Analysis:** Parser constructs initial parse tree
4. **Semantic Analysis:** Type attribution and symbol resolution (for typed languages)
5. **LST Construction:** Conversion to OpenRewrite's internal tree representation with full whitespace/comment preservation
6. **Marker Attachment:** Metadata (source sets, styles, compilation errors) attached to tree nodes

### Transformation Flow
1. **Recipe Validation:** Parameter validation and dependency resolution
2. **Visitor Construction:** Recipe creates appropriate visitor instances
3. **Tree Traversal:** Visitor walks LST in depth-first order
4. **Transformation Application:** Visitor methods modify tree nodes immutably
5. **Post-Processing:** Secondary visitors handle cleanup and formatting
6. **Result Collection:** Modified trees returned with change metadata

### Context Propagation
- **ExecutionContext:** Carries runtime state, metrics, and error handlers through transformation pipeline
- **Cursor:** Maintains parent chain during tree traversal for context-aware transformations
- **Markers:** Attach typed metadata to tree nodes for cross-cutting concerns
- **Styles:** Formatting and code style preferences propagated through tree structure

### Multi-Language Support
- Each language maintains its own AST structure under unified Tree interface
- Cross-language transformations handled through common abstraction layer
- Language-specific visitors extend base TreeVisitor with type-safe dispatch
- Parser builders configure language-specific compilation settings and classpath resolution