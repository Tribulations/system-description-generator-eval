### Manual Study Documentation

# Manual Study: JavaParser

## System Purpose

AssertJ is an open-source Java library that provides a rich set of fluent 
and expressive assertions for unit testing. Its main goal is to improve test 
readability and maintainability by allowing developers to write assertions 
in a human-readable, chainable format.

## Architectural Approach

AssertJ follows a modular and extensible architecture. The central module is 
assertj-core, which contains all the core assertion logic. Additional modules
provided extended support for specific libraries and frameworks, such as Guava, 
Swing, and JavaFX. The architecture is designed to be easily extensible, allowing
users to create custom assertions for their own types. The system is built around
the fluent interface design pattern, enabling a natural and readable syntax for
assertions. 
## Key Modules and Components
**Main modules:**
- `assertj-core` (Provides the foundation of all assertion functionality, 
  supporting various data types and structures. It includes entry point for 
  assertion methods for different types.)
- `assertj-guava` (Provides assertions for Guava collections and types. 
  Built on top of `assertj-core`.)
- `assertj-swing` (Provides assertions for Swing components. Built on top of 
  `assertj-core`.)
- `assertj-javafx` (Provides assertions for JavaFX components. Built on top of 
  `assertj-core`.)
- etc. 

**Testing modules:**
- src/test/java: Contains extensive unit and integration tests for 
  validating the assertions’ behavior in `assertj-core` module. 
- src/test/resources: Contains test resources, such as sample data files 
  and configuration files used in tests.
- It uses JUnit 4 and JUnit 5 for test coverage.
- Furthermore, it contains `assertj-tests` module, which is a 
  separate module that provides integration and performance tests for
  the core library.

## Notable Design Patterns and Techniques

1. **Fluent Interface Pattern**
   Central to the design, allowing method chaining to express assertions like:
   ````java
    assertThat(fruitList).hasSize(2).contains("Apple", "Banana");
    ````
2. **Factory Pattern**
   It is used to create a factory for creating error messages when as 
   assertion fails such as `org.assertj.core.error.BasicErrorMessageFactory` 
   many other error classes (e.g. `shouldBeEquql`, `shouldEndWith` etc.) 
   extends this class as a superclass. Another instance of factory 
   pattern can be found in the static entry points `(Assertions.assertThat(..
   .))` to create appropriate assertion objects based on input types.

3. **Template Method Pattern** 
   Common assertion behaviors are abstracted in base classes like AbstractAssert 
   and extended in concrete types (e.g., `StringAssert, ListAssert`).
4. **Generics and Type Safety**
   The system extensively uses Java Generics to ensure type safety across 
   assertion classes. This allows fluent method chaining while preserving 
   the correct return types. The heavy use of Java Generics also enables the 
   design of reusable base classes (e.g., `AbstractAssert`, 
   `AbstractIterableAssert`) that can operate across various data types. In 
   addition, the codebase demonstrates frequent use of the *Java Collections 
   Framework* and *Java Stream API* to process, filter, and validate data 
   during assertion evaluation.        

## Relationships and Dependencies
[Description of key relationships between components]
1. **assertj-core**
   - The core module that provides the foundation for all assertions.
   - Other modules depend on it for core functionality.
2. **assertj-guava**
   - Depends on assertj-core for assertion logic.
   - Provides additional assertions for Guava collections and types.
3. **assertj-swing**
    - Depends on assertj-core for assertion logic.
    - Provides additional assertions for Swing components.
4. **assertj-javafx**
   - Both depend on assertj-core for core assertion functionality.
   - Provide additional assertions for JavaFX.

## Important Implementation Details
[Notable implementation aspects relevant to high-level understanding (If applicable)]
- Custom Comparators: Users can inject comparators to override default 
equality checks using `.usingComparator(...)`. 
- Soft Assertions: Allows multiple assertions to be evaluated and reports 
  all failures together. 
- Assumption Support: Built-in support for assumption-based testing via 
  `Assumptions.assumeThat(...)`.

## References
- [README](https://github.com/assertj/assertj/blob/main/README.md)
- [AssertJ GitHub]()
- [AssertJ API Documentation](https://assertj.github.io/doc/)
- [AssertJ Core API javadoc](https://www.javadoc.io/doc/org.assertj/assertj-core/latest/index.html)

---