# Apache Paimon System Overview

## System Purpose
Apache Paimon is a distributed data lake storage system designed for streaming and batch data processing. It provides table storage capabilities with ACID transactions, schema evolution, and integration with compute engines like Apache Flink and Apache Spark.

## Key Components & Responsibilities

### 1. **Factory (org.apache.paimon.mergetree.compact)**
- Creates and manages various file system components including manifest files, index files, and data formats
- Handles serialization and deserialization of metadata structures
- Implements the Factory pattern for multiple object types (EventParser, ManifestFile, IndexManifestFile, ManifestList, DataFormat, SimpleColStatsCollector)
- Manages file format creation and statistics collection

### 2. **Builder (org.apache.paimon.spark.procedure)**
- Constructs complex objects for Spark procedures including schemas, data splits, and row types
- Implements the Builder pattern for multiple data structures
- Handles configuration of streaming vs batch processing modes
- Manages bucket configuration and parallelism settings

### 3. **FlinkCatalog (org.apache.paimon.flink)**
- Serves as the primary catalog interface for Apache Flink integration
- Manages database and table metadata operations (create, drop, alter)
- Handles table schema changes and DDL operations
- Implements Flink's AbstractCatalog interface for seamless integration
- Manages materialized tables, views, and partition metadata

### 4. **Reader (org.apache.paimon.fileindex)**
- Reads file index data for query optimization
- Implements both source reader and file index reader interfaces
- Provides methods to read all index entries as key-value maps
- Supports closeable resource management

### 5. **CoreOptions (org.apache.paimon)**
- Central configuration management class containing all system-wide options
- Defines settings for compaction, file formats, memory management, snapshots, and tags
- Provides type-safe access to configuration values
- Implements serializable configuration state

### 6. **AWS S3 Transform Handlers (com.amazonaws.services.s3.model.transform)**
- Handle XML parsing and transformation of S3 API responses
- Implement SAX-based parsing for various S3 operations (CopyObject, CompleteMultipartUpload, BucketLocation, ListBucket, etc.)
- Manage server-side encryption results and versioning information
- Process bucket configurations (logging, versioning, website, ACLs)

## Core Technologies & Dependencies

### Primary Technologies:
- **Apache Flink**: Stream processing integration
- **Apache Spark**: Batch processing integration
- **Apache Parquet**: Columnar file format
- **ORC**: Alternative columnar format
- **AWS SDK**: S3 storage backend support

### Key Dependencies:
- Jackson (JSON processing)
- Guava (utility libraries)
- Apache Hadoop (file system abstraction)
- SLF4J (logging)
- Apache Commons (utilities)

## Architecture

### Layered Architecture:
1. **Catalog Layer**: Manages metadata, schemas, and table definitions (FlinkCatalog)
2. **Storage Layer**: Handles file I/O, manifests, and data files (Factory, CoreOptions)
3. **Compute Integration Layer**: Provides APIs for Flink and Spark (Builder, Reader)
4. **Index Layer**: Manages file indexes for query optimization (Reader, FileIndexOptions)
5. **Cloud Storage Layer**: Integrates with S3 and other object stores (AWS handlers)

### Design Patterns:
- **Factory Pattern**: Extensive use for creating file formats, readers, and writers
- **Builder Pattern**: Complex object construction for Spark procedures
- **Handler Pattern**: SAX-based XML processing for S3 responses
- **Catalog Pattern**: Metadata management following Flink's catalog interface

## Data Flow

### Write Path:
1. Data enters through Flink/Spark compute engines
2. CoreOptions determines file format, compression, and storage settings
3. Factory creates appropriate writers and serializers
4. Data is written to manifest files and data files
5. Metadata is updated in the catalog (FlinkCatalog)
6. File indexes are created for query optimization

### Read Path:
1. Query submitted through Flink/Spark
2. FlinkCatalog retrieves table metadata and schema
3. Reader components access file indexes to optimize data access
4. Factory creates appropriate readers based on file format
5. Data is streamed or batched to compute engine
6. Statistics and indexes guide partition pruning and filtering

### Metadata Flow:
1. Schema changes processed through FlinkCatalog
2. Manifest files track data file locations and statistics
3. Index files maintain column-level indexes
4. Snapshot management tracks table versions over time
5. CoreOptions configuration propagates to all components

### Cloud Storage Integration:
1. S3 handlers parse API responses for bucket operations
2. File paths resolved through PathFactory
3. Data files stored in S3 with manifest tracking
4. Encryption and versioning managed through AWS handlers