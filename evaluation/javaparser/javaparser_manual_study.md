### Manual Study Documentation

# Manual Study: JavaParser

## System Purpose

JavaParser is an open-source parsing library written in Java. It allows interacting with Java source code as a Java object representation in a Java environment i.e., as an Abstract Syntax Tree (AST). JavaParser also provides convenient ways to identify interesting patterns in code by navigating the AST called "Visitor Support" in JavaParser terminology. A final main feature of JavaParser is the ability to manipulate the structure of source code and write the result to a file, enabling the functionality to build code generation software.

## Architectural Approach

JavaParser consists of 5 Main modules and 3 testing modules (identified by examining the project directory structure, analayze dependencies tool, and pom.xml file). Clear separation of concerns using a modular approach. Built around the javaparser-core module. 


## Key Modules and Components
**Main modules:**
- javaparser-core (Main module all other modules depend on)
- javaparser-core-generators 
- javaparser-core-metamodel-generator
- javaparser-core-serialization
- javaparser-symbol-solver-core

**Testing modules:**
- javaparser-core-testing
- javaparser-core-testing-bdd
- javaparser-symbol-solver-testing

## Notable Design Patterns and Techniques

### Implements Visitor Pattern

1. **Visitor interfaces:**
- com.github.javaparser.ast.visitor.GenericVisitor
- com.github.javaparser.ast.visitor.GenericVisitor.VoidVisitor

**Visitable interfaces**
com.github.javaparser.ast.visitor.Visitable

**Concrete visitable/visitor implementations**
- com.github.javaparser.ast.visitor.ModifierVisitor
- com.github.javaparser.ast.visitor.NodeFinderVisitor
- com.github.javaparser.ast.visitor.TreeVisitor

2. **Observer pattern**

**Observer interfaces**
- com.github.javaparser.ast.observer.AstObserver
- com.github.javaparser.ast.observer.Observable

## Relationships and Dependencies
[Description of key relationships between components]

1. **Core module**
- The Core module has no dependencies on other modules

2. **Generators module**
- Depends on the Core module.

3. **Metamodel Generator module**
- Depends on the Core module.

4. **Serialization module**
- Depends on the Core module.

5. **Symbol solver module**
- Depends on the Core module.

**Inheritance hierarchy**
Node is the base class of the AST node hierarchy with concrete nodes such as ClassOrInterfaceDeclaration, MethodCallExpr, MethodDeclaration, and many others.

## Important Implementation Details
[Notable implementation aspects relevant to high-level understanding (If applicable)]

## References
- [JavaParser: Visited](https://leanpub.com/javaparservisited)
- [README](https://github.com/javaparser/javaparser/blob/master/doc/readme.md)
- [Component diagram](https://github.com/javaparser/javaparser/blob/master/doc/component_diagram.puml)
- [JavaParser GitHub](https://github.com/javaparser/javaparser)

---
