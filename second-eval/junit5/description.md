
# JUnit 5 System Overview

## System Purpose
JUnit 5 is a comprehensive testing framework for Java applications that provides infrastructure for writing, discovering, executing, and reporting on automated tests. It supports parameterized testing, dynamic test generation, nested test structures, and parallel execution capabilities.

## Key Components & Responsibilities

### Test Engine & Execution
- **JupiterEngineExecutionContext**: Manages the execution state and configuration for test runs
- **VintageExecutor**: Provides backward compatibility by executing JUnit 4 tests within the JUnit 5 framework
- **EngineDiscoveryOrchestrator**: Coordinates test discovery across multiple test engines and applies filters

### Test Discovery & Resolution
- **ClassSelectorResolver**: Resolves class-based test selectors to test descriptors
- **MethodSelectorResolver**: Resolves method-based test selectors for individual test methods
- **EngineDiscoveryRequestResolver**: Processes discovery requests and builds the test execution tree
- **SelectorResolver**: Core interface for converting discovery selectors into executable test descriptors

### Parameterized Testing
- **DefaultParameterDeclarations**: Manages parameter declarations for parameterized tests
- **CsvFileArgumentsProvider**: Provides test arguments from CSV files
- **ArgumentSetNameFormatter**: Formats display names for parameterized test invocations
- **ResolverFacade**: Coordinates parameter resolution and argument conversion

### Extension System
- **MutableExtensionRegistry**: Manages registration and lifecycle of test extensions
- **AbstractExtensionContext**: Provides context information to extensions during test execution
- **TempDirectory**: Built-in extension for managing temporary directories in tests

### Reporting & Listeners
- **XmlReportWriter**: Generates XML test reports in legacy format
- **DiscoveryIssueCollector**: Collects and reports issues encountered during test discovery
- **LauncherDiscoveryListener**: Receives notifications about discovery events

### Suite & Platform Integration
- **SuiteLauncherDiscoveryRequestBuilder**: Builds discovery requests for test suites
- **JUnitPlatform**: Runner for executing JUnit Platform tests
- **LauncherDiscoveryRequestBuilder**: Constructs discovery requests with filters and selectors

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core programming language with reflection and annotation processing
- **JUnit Platform**: Foundation for launching testing frameworks
- **JUnit Jupiter API**: Modern testing API with annotations and assertions

### Key Dependencies
- **Apiguardian**: API stability annotations
- **Picocli**: Command-line interface parsing
- **Univocity Parsers**: CSV parsing for parameterized tests
- **ClassGraph**: Classpath scanning and class discovery
- **OpenTest4J**: Open test reporting format

### File System & I/O
- **Java NIO**: File operations and path management
- **XML Stream API**: XML report generation

## Architecture

### Layered Structure
1. **API Layer**: Public interfaces and annotations (`@Test`, `@ParameterizedTest`, `@ExtendWith`)
2. **Engine Layer**: Test execution engines (Jupiter, Vintage)
3. **Platform Layer**: Discovery, filtering, and launcher infrastructure
4. **Extension Layer**: Pluggable extension points for customization

### Discovery Pipeline
```
Discovery Request → Selector Resolution → Descriptor Tree → Filter Application → Execution Plan
```

### Extension Mechanism
Extensions hook into test lifecycle through callback interfaces:
- `BeforeAllCallback`, `BeforeEachCallback`
- `ParameterResolver`
- `TestTemplateInvocationContextProvider`

## Data Flow

### Test Discovery Flow
1. **Request Creation**: Discovery selectors (class, method, package) are specified
2. **Selector Resolution**: Resolvers convert selectors to test descriptors
3. **Tree Building**: Descriptors are organized into hierarchical test tree
4. **Filter Application**: Discovery and post-discovery filters prune the tree
5. **Execution Planning**: Final test plan is prepared for execution

### Test Execution Flow
1. **Context Initialization**: Extension context and registry are established
2. **Extension Callbacks**: `BeforeAll` extensions execute
3. **Test Instance Creation**: Test class is instantiated
4. **Parameter Resolution**: Method parameters are resolved via extensions
5. **Test Invocation**: Actual test method executes
6. **Result Collection**: Execution results are captured and reported
7. **Cleanup**: `AfterAll` and resource cleanup extensions execute

### Parameterized Test Flow
1. **Argument Provider**: Sources provide argument sets (CSV, method, annotation)
2. **Parameter Declaration**: Method parameters are analyzed and mapped
3. **Conversion**: Arguments are converted to parameter types
4. **Invocation**: Test method executes once per argument set
5. **Display Name Formatting**: Each invocation receives formatted display name

### Reporting Flow
1. **Listener Notification**: Execution events trigger listener callbacks
2. **Result Aggregation**: Test results are collected and aggregated
3. **Report Generation**: XML/console reports are generated
4. **Issue Reporting**: Discovery and execution issues are logged with severity levels