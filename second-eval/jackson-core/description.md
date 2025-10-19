# Jackson-Core System Overview

## System Purpose
Jackson-core is a high-performance JSON processing library for Java that provides low-level streaming APIs for reading (parsing) and writing (generating) JSON content. It serves as the foundation for the Jackson data-binding framework.

## Key Components & Responsibilities

### **Parsing Components**
- **JsonParser**: Abstract base class for all JSON parsers, providing token-based reading of JSON content
- **ParserBase & ParserMinimalBase**: Base implementations providing common parsing functionality
- **JsonParserBase**: JSON-specific parser base with UTF-8 handling capabilities
- **ReaderBasedJsonParser**: Parses JSON from character streams (Reader)
- **UTF8StreamJsonParser & UTF8DataInputJsonParser**: Parse JSON from UTF-8 encoded byte streams
- **NonBlockingJsonParser & NonBlockingByteBufferJsonParser**: Support asynchronous, non-blocking JSON parsing

### **Generation Components**
- **JsonGenerator**: Abstract base class for JSON writers, providing methods to write JSON content
- **GeneratorBase**: Common generator functionality implementation
- **JsonGeneratorImpl**: JSON-specific generator base class
- **WriterBasedJsonGenerator**: Writes JSON to character streams
- **UTF8JsonGenerator**: Writes JSON directly to UTF-8 encoded byte streams

### **Factory & Configuration**
- **JsonFactory**: Main entry point for creating parsers and generators
- **TokenStreamFactory**: Abstract factory base class
- **JsonFactoryBuilder & TSFBuilder**: Builder pattern implementation for factory configuration
- **IOContext**: Manages I/O resources, buffer allocation, and recycling

### **Symbol Management**
- **ByteQuadsCanonicalizer**: Canonicalizes field names from UTF-8 byte sequences for parsers
- **CharsToNameCanonicalizer**: Canonicalizes field names from character arrays for parsers
- **Name, Name1, Name2, Name3, NameN**: Optimized name representations for different lengths

### **Filtering & Delegation**
- **TokenFilter**: Enables selective filtering of JSON content during parsing
- **FilteringParserDelegate**: Wraps parsers to apply filtering logic
- **FilteringGeneratorDelegate**: Wraps generators to apply filtering logic
- **TokenFilterContext**: Maintains filtering state during parsing

### **I/O & Encoding**
- **CharTypes**: Character classification and escaping tables
- **CharacterEscapes**: Customizable character escaping strategies
- **UTF8Writer & UTF32Reader**: Handle UTF encoding conversions
- **NumberOutput & NumberInput**: Optimized number formatting and parsing
- **BigDecimalParser & BigIntegerParser**: High-performance parsing of large numbers

### **Constraints & Validation**
- **StreamReadConstraints**: Enforces limits on document size, nesting depth, and token counts
- **StreamWriteConstraints**: Enforces limits on output generation
- **DupDetector**: Detects duplicate object keys when enabled

### **Context & Location**
- **JsonStreamContext**: Tracks current position in JSON structure (object/array/root)
- **JsonReadContext & JsonWriteContext**: Maintain parsing and generation state
- **JsonLocation**: Represents position in source (line, column, byte offset)
- **ContentReference**: References source content for error reporting

## Core Technologies & Dependencies

### **Java Standard Library**
- Java I/O streams (InputStream, OutputStream, Reader, Writer)
- Java NIO (ByteBuffer)
- Java math (BigDecimal, BigInteger)
- Java concurrency (AtomicReference, atomic types)

### **External Dependencies**
- **ch.randelshofer.fastdoubleparser**: High-performance number parsing (JavaDoubleParser, JavaFloatParser, JavaBigDecimalParser, JavaBigIntegerParser)

### **Internal Utilities**
- **BufferRecycler**: Reuses byte and character buffers to reduce allocation overhead
- **TextBuffer**: Efficient text accumulation during parsing
- **ByteArrayBuilder**: Builds byte arrays incrementally
- **RecyclerPool**: Manages buffer recycler instances

## Architecture

Jackson-core follows a **streaming architecture** with three main layers:

1. **Factory Layer**: JsonFactory creates and configures parser/generator instances
2. **Streaming Layer**: JsonParser and JsonGenerator provide token-based streaming APIs
3. **Support Layer**: Symbol tables, I/O utilities, and buffer management support streaming operations

The system uses **template method pattern** extensively, with abstract base classes defining the parsing/generation flow and concrete implementations handling format-specific details.

## Data Flow

### **Parsing Flow**
1. Client creates JsonParser via JsonFactory from an input source (byte array, stream, reader)
2. JsonFactory allocates buffers via IOContext and BufferRecycler
3. Parser reads input incrementally, tokenizing JSON structure
4. Field names are canonicalized through ByteQuadsCanonicalizer or CharsToNameCanonicalizer
5. Parser returns tokens (START_OBJECT, FIELD_NAME, VALUE_STRING, etc.) via nextToken()
6. Client retrieves values using type-specific methods (getText(), getIntValue(), etc.)
7. On close, buffers are returned to BufferRecycler for reuse

### **Generation Flow**
1. Client creates JsonGenerator via JsonFactory targeting an output destination
2. JsonFactory allocates output buffers via IOContext
3. Client calls write methods (writeStartObject(), writeFieldName(), writeString(), etc.)
4. Generator maintains context via JsonWriteContext to track structure validity
5. Content is encoded and buffered, then flushed to output stream
6. Character escaping is applied based on CharacterEscapes configuration
7. On close, buffers are flushed and returned to BufferRecycler

### **Filtering Flow**
1. FilteringParserDelegate wraps a JsonParser with a TokenFilter
2. During nextToken(), filter determines which tokens to expose or skip
3. TokenFilterContext maintains filter state across nested structures
4. Filtered tokens are transparently skipped, presenting a filtered view to the client