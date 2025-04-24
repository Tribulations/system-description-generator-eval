"""
Contains the generated description and the JSON used in the prompt to LLM when generating description for SDG itself using Anthropic API.
"""

generated_description = """
System Description: Here's a structured summary of the system:

**System Purpose:**
The system (sdg) is a Java-based knowledge graph generator and analyzer that processes Java source code to create and manage graph-based representations of software systems, with capabilities for both visualization and LLM-based analysis.

**Key Components & Responsibilities:**

1. InputView (UI Layer):
- Provides a graphical interface extending JFrame
- Handles user interactions for file input, processing, and displaying results
- Manages loading indicators and output display

2. GraphDatabaseOperations (Data Layer):
- Manages Neo4j database operations
- Handles CRUD operations for graph nodes and relationships
- Provides transaction and batch processing capabilities
- Creates and manages nodes for classes, methods, control flow, and relationships

3. KnowledgeGraphService (Service Layer):
- Orchestrates the knowledge graph processing workflow
- Integrates with LLM services (Gemini and Claude)
- Manages asynchronous processing of source code analysis
- Handles reactive processing using RxJava

**Core Technologies & Dependencies:**

1. Database:
- Neo4j (Graph Database)
- Neo4j Java Driver

2. UI Framework:
- Swing (Java GUI components)

3. Processing & Integration:
- RxJava for reactive programming
- JavaParser for AST analysis
- CompletableFuture for async operations

4. AI Integration:
- Gemini API
- Claude API

5. Utility:
- Custom logging framework
- Java standard libraries

The system implements a three-tier architecture (UI, Service, Data) with clear separation of concerns and modern async processing capabilities.
"""

sdg_llm_json_input = """{
  "systemName" : "sdg",
  "classes" : [ {
    "name" : "InputView",
    "packageName" : "com.sdg.view",
    "extendedClasses" : [ "JFrame" ],
    "implementedInterfaces" : [ ],
    "methods" : [ {
      "name" : "setOutputText",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "setText"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "clearLoadingIndicator",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "repaint"
      }, {
        "calledMethod" : "invokeLater"
      }, {
        "calledMethod" : "revalidate"
      }, {
        "calledMethod" : "setVisible"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "addProcessListener",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "addActionListener"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "addBrowseListener",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "addActionListener"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "getInputPath",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "getText"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "addDecListener",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "addActionListener"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "clearOutputArea",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "setText"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "getDescButton",
      "visibility" : "public",
      "methodCalls" : [ ],
      "controlFlow" : [ ]
    }, {
      "name" : "getProcessButton",
      "visibility" : "public",
      "methodCalls" : [ ],
      "controlFlow" : [ ]
    }, {
      "name" : "appendOutputText",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "getLength"
      }, {
        "calledMethod" : "append"
      }, {
        "calledMethod" : "setCaretPosition"
      }, {
        "calledMethod" : "getDocument"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "showLoadingIndicator",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "invokeLater"
      }, {
        "calledMethod" : "setVisible"
      }, {
        "calledMethod" : "setText"
      }, {
        "calledMethod" : "repaint"
      }, {
        "calledMethod" : "revalidate"
      } ],
      "controlFlow" : [ ]
    } ],
    "fields" : [ ],
    "imports" : [ "java.awt.GridBagLayout", "java.awt.Insets", "java.awt.GridBagConstraints", "java.awt.event.FocusAdapter", "java.awt.Font", "javax.swing.SwingUtilities", "javax.swing.JButton", "javax.swing.JTextField", "java.awt.event.ActionListener", "javax.swing.JLabel", "java.awt.BorderLayout", "java.awt.Dimension", "javax.swing.JFrame", "javax.swing.border.EmptyBorder", "java.awt.event.FocusEvent", "javax.swing.JPanel", "javax.swing.JProgressBar", "javax.swing.JTextArea", "javax.swing.JScrollPane", "java.awt.Color" ]
  }, {
    "name" : "GraphDatabaseOperations",
    "packageName" : "com.sdg.graph",
    "extendedClasses" : [ ],
    "implementedInterfaces" : [ "AutoCloseable" ],
    "methods" : [ {
      "name" : "close",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "info"
      }, {
        "calledMethod" : "close"
      }, {
        "calledMethod" : "endBatchSession"
      }, {
        "calledMethod" : "getClass"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "rollbackBatchTransaction",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "rollback"
      }, {
        "calledMethod" : "close"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "startBatchTransaction",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "beginTransaction"
      }, {
        "calledMethod" : "warn"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "commitBatchTransaction"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "startBatchSession",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "info"
      }, {
        "calledMethod" : "warn"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "session"
      }, {
        "calledMethod" : "endBatchSession"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "isBatchTransactionActive",
      "visibility" : "public",
      "methodCalls" : [ ],
      "controlFlow" : [ ]
    }, {
      "name" : "createControlFlowNode",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "debug"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "createMethodNode",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "debug"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "endBatchSession",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "close"
      }, {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "info"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "createInheritanceRelationship",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "getClass"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "createInterfaceImplementation",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "getClass"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "getDriver",
      "visibility" : "public",
      "methodCalls" : [ ],
      "controlFlow" : [ ]
    }, {
      "name" : "isBatchSessionActive",
      "visibility" : "public",
      "methodCalls" : [ ],
      "controlFlow" : [ ]
    }, {
      "name" : "createMethodCallNode",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "parameters"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "createClassNode",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "getClass"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "deleteAllData",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "info"
      }, {
        "calledMethod" : "run"
      }, {
        "calledMethod" : "session"
      }, {
        "calledMethod" : "executeWrite"
      }, {
        "calledMethod" : "getClass"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "commitBatchTransaction",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "close"
      }, {
        "calledMethod" : "debug"
      }, {
        "calledMethod" : "commit"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "createImportRelationship",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "debug"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "createClassField",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "parameters"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "debug"
      } ],
      "controlFlow" : [ ]
    } ],
    "fields" : [ ],
    "imports" : [ "org.neo4j.driver.Value", "org.neo4j.driver.GraphDatabase", "org.neo4j.driver.Transaction", "org.neo4j.driver.Values.parameters", "org.neo4j.driver.Driver", "com.sdg.logging.LoggerUtil", "org.neo4j.driver.Session", "org.neo4j.driver.AuthTokens" ]
  }, {
    "name" : "KnowledgeGraphService",
    "packageName" : "com.sdg.graph",
    "extendedClasses" : [ ],
    "implementedInterfaces" : [ "AutoCloseable" ],
    "methods" : [ {
      "name" : "generateLLMResponseAsync",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "whenComplete"
      }, {
        "calledMethod" : "onSuccess"
      }, {
        "calledMethod" : "generateHighLevelDescriptionAsync"
      }, {
        "calledMethod" : "onError"
      }, {
        "calledMethod" : "create"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "processKnowledgeGraph",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "processFilesRx"
      }, {
        "calledMethod" : "doOnNext"
      }, {
        "calledMethod" : "info"
      }, {
        "calledMethod" : "getClass"
      }, {
        "calledMethod" : "observeOn"
      }, {
        "calledMethod" : "deleteAllData"
      }, {
        "calledMethod" : "doOnComplete"
      }, {
        "calledMethod" : "doOnError"
      }, {
        "calledMethod" : "io"
      }, {
        "calledMethod" : "currentTimeMillis"
      } ],
      "controlFlow" : [ ]
    }, {
      "name" : "close",
      "visibility" : "public",
      "methodCalls" : [ {
        "calledMethod" : "info"
      }, {
        "calledMethod" : "close"
      }, {
        "calledMethod" : "endBatchSession"
      }, {
        "calledMethod" : "getClass"
      } ],
      "controlFlow" : [ ]
    } ],
    "fields" : [ ],
    "imports" : [ "io.reactivex.rxjava3.schedulers.Schedulers", "io.reactivex.rxjava3.core.Observable", "java.util.concurrent.atomic.AtomicInteger", "java.nio.file.Files", "io.reactivex.rxjava3.core.Single", "java.util.concurrent.CompletableFuture", "java.nio.file.Path", "com.sdg.logging.LoggerUtil", "com.sdg.ast.JavaFileParser", "com.sdg.ast.ASTAnalyzerConfig", "com.sdg.ast.ASTAnalyzer", "com.sdg.llm.GeminiApiClient", "com.sdg.model.InputHandler", "com.sdg.llm.LLMService", "com.sdg.model.InputHandler.ProcessingResult", "java.io.IOException", "com.github.javaparser.ast.CompilationUnit", "com.sdg.llm.ClaudeApiClient" ]
  } ]
}
"""