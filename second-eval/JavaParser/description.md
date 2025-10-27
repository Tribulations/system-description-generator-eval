# JavaParser System - High-Level Summary

## 1. System Purpose

JavaParser is a Java source code parsing and manipulation library that analyzes, transforms, and generates Java code programmatically. It provides a complete Abstract Syntax Tree (AST) representation of Java source files, enabling static analysis, code generation, refactoring, and symbol resolution.

## 2. Key Components & Responsibilities

### Core Parsing Components
- **GeneratedJavaParser**: The main parser implementation that converts Java source code into AST nodes. Handles all Java language constructs including expressions, statements, declarations, and modules.
- **Node & Subclasses**: The AST node hierarchy representing all Java language elements (Expression, Statement, Type, BodyDeclaration, etc.). Each node type corresponds to a specific Java construct.

### AST Navigation & Traversal
- **NodeList**: A specialized list implementation for managing collections of AST nodes with parent-child relationships.
- **Iterator Implementations** (BreadthFirstIterator, PreOrderIterator, PostOrderIterator, DirectChildrenIterator, ParentsVisitor): Provide different traversal strategies through the AST.
- **Level**: Manages hierarchical traversal state during tree navigation.

### Visitor Pattern Infrastructure
- **NodeFinderVisitor**: Extends VoidVisitorAdapter to locate specific nodes within the AST.
- **Visitor interfaces**: Support the visitor pattern for AST traversal and transformation operations.

### Symbol Resolution
- **AbstractJavaParserContext**: Base implementation for resolving symbols (types, methods, variables) within specific AST contexts.
- **TypeExtractor**: Extracts and resolves type information from expressions and declarations.
- **JavaParserEnumDeclaration, JavaParserRecordDeclaration, JavaParserInterfaceDeclaration**: Provide symbol resolution capabilities for specific declaration types.

### Type System
- **Type Hierarchy** (ClassOrInterfaceType, ReferenceType, etc.): Represents Java's type system in the AST.
- **ResolvedReferenceType**: Represents fully resolved type information including generics, type parameters, and inheritance relationships.

### Declaration Representations
- **MethodDeclaration, FieldDeclaration, Parameter, VariableDeclarator**: Represent method, field, and variable declarations.
- **ClassOrInterfaceDeclaration, RecordDeclaration, EnumConstantDeclaration**: Represent type declarations.
- **CallableDeclaration**: Abstract base for methods and constructors.

### Reflection & Javassist Integration
- **ReflectionClassDeclaration, ReflectionRecordDeclaration**: Bridge between JavaParser's AST and Java's reflection API.
- **JavassistRecordDeclaration**: Integrates with Javassist bytecode manipulation library for enhanced type resolution.

### Lexical Preservation
- **LexicalPreservingPrinter**: Maintains original formatting and whitespace when modifying AST nodes.
- **Observer**: Tracks AST changes to preserve lexical information during transformations.

### Compilation Unit Management
- **CompilationUnit**: Root node representing a complete Java source file, including package declaration, imports, and type declarations.
- **Storage**: Associates compilation units with their file system locations.

### Expression & Statement Nodes
- **MethodCallExpr, ObjectCreationExpr, FieldAccessExpr, InstanceOfExpr**: Represent various expression types.
- **Statement, BlockStmt, SwitchEntry, ExplicitConstructorInvocationStmt**: Represent executable statements.

### Specialized Method Declarations
- **ValuesMethod, ValueOfMethod**: Synthetic method declarations for enum types.
- **ImplicitGetterMethod**: Represents auto-generated getter methods for record components.
- **CompactConstructorDeclaration**: Represents compact constructors in record types.

## 3. Core Technologies & Dependencies

### Primary Technologies
- **Java**: The implementation language and target parsing language.
- **JavaCC/JJTree**: Parser generator used to create GeneratedJavaParser from grammar definitions.

### Key Dependencies
- **Javassist**: Bytecode manipulation library for enhanced type resolution.
- **Java Reflection API**: Used for runtime type information and symbol resolution.
- **Google Guava**: Utility library (evidenced by ImmutableList usage in TypeExtractor).

### Design Patterns
- **Visitor Pattern**: Core pattern for AST traversal and transformation.
- **Observer Pattern**: Used for tracking AST modifications (Observable, AstObserver).
- **Factory Pattern**: JavaParserFactory creates context and declaration objects.

## 4. Architecture

### Layered Architecture

**Layer 1: Parsing Layer**
- GeneratedJavaParser converts source text into AST nodes
- Token management and lexical analysis

**Layer 2: AST Representation Layer**
- Node hierarchy representing all Java language constructs
- Parent-child relationships and tree structure maintenance
- NodeList for managing node collections

**Layer 3: Navigation & Traversal Layer**
- Multiple iterator implementations for different traversal strategies
- Visitor pattern infrastructure for AST processing

**Layer 4: Symbol Resolution Layer**
- Context-based symbol resolution (AbstractJavaParserContext)
- Type resolution using reflection, Javassist, and AST analysis
- Declaration representations with resolution capabilities

**Layer 5: Transformation & Output Layer**
- LexicalPreservingPrinter for format-preserving modifications
- Standard printing for code generation

### Component Interaction Model
- **Bidirectional Parent-Child Links**: Nodes maintain references to parents and children
- **Context-Aware Resolution**: Symbol resolution uses context objects that understand scope
- **Lazy Type Resolution**: Types are resolved on-demand using LazyType wrapper
- **Observer-Based Change Tracking**: Modifications trigger observer notifications for lexical preservation

## 5. Data Flow

### Parsing Flow
1. **Input**: Java source code (String, File, or InputStream)
2. **Tokenization**: GeneratedJavaParser tokenizes input using JavaToken
3. **AST Construction**: Parser creates Node hierarchy (CompilationUnit as root)
4. **Parent Assignment**: Nodes establish bidirectional parent-child relationships
5. **Output**: Fully constructed AST ready for analysis or transformation

### Symbol Resolution Flow
1. **Resolution Request**: Client calls resolve() on a Node (e.g., MethodCallExpr, Type)
2. **Context Retrieval**: Node obtains its resolution Context via getContext()
3. **Symbol Lookup**: Context searches through scopes (local → enclosing → imports → type solver)
4. **Type Solver Query**: For external types, TypeSolver consults reflection or Javassist
5. **Declaration Return**: Resolved declaration (ResolvedMethodDeclaration, ResolvedTypeDeclaration) returned
6. **Caching**: Results may be cached to avoid redundant resolution

### Type Resolution Flow
1. **Type Reference**: AST contains Type nodes (ClassOrInterfaceType, etc.)
2. **Conversion Request**: toResolvedType() called on Type node
3. **Symbol Resolver Access**: getSymbolResolver() retrieves configured resolver
4. **Declaration Resolution**: Type name resolved to ResolvedReferenceTypeDeclaration
5. **Type Construction**: ResolvedReferenceType created with type parameters and bounds
6. **Inheritance Resolution**: Superclasses and interfaces resolved recursively

### Modification Flow (with Lexical Preservation)
1. **Setup**: LexicalPreservingPrinter.setup() registers observers on AST
2. **Modification**: Client modifies AST nodes (add/remove/change)
3. **Observer Notification**: PropagatingAstObserver detects changes
4. **Difference Calculation**: LexicalDifferenceCalculator computes minimal changes
5. **Token Adjustment**: Original tokens updated to reflect modifications
6. **Output**: Modified code printed with preserved formatting

### Traversal Flow
1. **Iterator Creation**: Client creates iterator (PreOrderIterator, etc.) with root node
2. **Traversal Strategy**: Iterator applies specific traversal algorithm
3. **Node Visitation**: Each node visited in defined order
4. **Visitor Application**: Optional visitor pattern applied during traversal
5. **Result Collection**: Matching nodes or transformation results collected