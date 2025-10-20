# GATK System Overview

## System Purpose
GATK (Genome Analysis Toolkit) is a comprehensive genomics analysis platform designed for variant discovery and genotyping in high-throughput sequencing data. The system processes DNA/RNA sequencing reads to identify structural variants, single nucleotide polymorphisms (SNPs), insertions/deletions (indels), and copy number variations (CNVs).

## Key Components & Responsibilities

### 1. **Core Engine Components**
- **GATKTool**: Base class for all analysis tools, manages reference data, feature inputs, and output handling
- **GATKSparkTool**: Extends GATKTool for distributed processing using Apache Spark
- **ReadWalker/VariantLocusWalker**: Traversal engines that iterate over reads or variant positions
- **AssemblyRegionWalker**: Processes genomic regions requiring local assembly for variant calling

### 2. **Variant Calling Pipeline**
- **HaplotypeCaller/HaplotypeCallerEngine**: Primary variant caller using local de-novo assembly
- **Mutect2Engine**: Somatic variant caller for tumor-normal pairs
- **GenotypeGVCFs**: Joint genotyping tool for combining single-sample GVCFs
- **ReferenceConfidenceModel**: Generates reference confidence calls (GVCF mode)

### 3. **Structural Variant Discovery**
- **StructuralVariationDiscoveryPipelineSpark**: End-to-end SV detection pipeline
- **FindBreakpointEvidenceSpark**: Identifies breakpoint evidence from read pairs and split reads
- **ContigChimericAlignmentIterativeInterpreter**: Analyzes assembled contigs for complex variants
- **SVConcordance**: Validates and compares SV callsets

### 4. **Copy Number Analysis**
- **ModelSegments**: Segments genome and models copy ratios and allelic fractions
- **GermlineCNVCaller**: Detects germline copy number variants
- **PostprocessGermlineCNVCalls**: Filters and annotates CNV calls
- **FilterIntervals**: Quality control for interval-based analysis

### 5. **Data Processing & Quality Control**
- **ReadsPipelineSpark**: Distributed read processing (alignment, deduplication, BQSR)
- **MarkDuplicatesSpark**: Identifies and marks PCR/optical duplicates
- **BaseRecalibrator/ApplyBQSR**: Base quality score recalibration
- **FilterAlignmentArtifacts**: Removes alignment-induced false positives

### 6. **Functional Annotation**
- **GencodeFuncotationFactory**: Annotates variants with GENCODE gene information
- **MafOutputRenderer**: Generates MAF (Mutation Annotation Format) output
- **DataSourceFuncotationFactory**: Framework for pluggable annotation sources

### 7. **Data Management**
- **GenomicsDBImport**: Imports VCFs into GenomicsDB for efficient storage
- **FeatureDataSource**: Unified interface for reading genomic features (VCF, BED, etc.)
- **ReadsDataSource**: Manages BAM/CRAM file access with filtering

### 8. **Variant Quality Score Recalibration**
- **ScoreVariantAnnotations**: Machine learning-based variant filtering
- **VariantEvalEngine**: Comprehensive variant evaluation and stratification

## Core Technologies & Dependencies

### Primary Technologies
- **Java**: Core implementation language
- **Apache Spark**: Distributed computing framework for scalable processing
- **Scala**: Used for Spark integration components
- **Python**: External scripts for machine learning models

### Key Libraries
- **HTSJDK**: SAM/BAM/VCF/BCF file format handling
- **BWA-MEM**: Read alignment library
- **Fermi-Lite**: Local assembly engine
- **Smith-Waterman**: Sequence alignment algorithms
- **Apache Commons Math**: Statistical computations
- **Kryo**: Serialization framework for Spark

### External Dependencies
- **GenomicsDB**: Efficient variant storage and retrieval
- **Reference Genome**: FASTA format with indices (.fai, .dict)
- **GATK Resource Bundle**: Known variants, training sets, intervals

## Architecture

### Layered Architecture
1. **Command Line Interface Layer**: Barclay argument parsing framework
2. **Tool Layer**: Specific analysis implementations (HaplotypeCaller, Mutect2, etc.)
3. **Engine Layer**: Traversal engines and data access patterns
4. **Data Access Layer**: Feature readers, reference access, read sources
5. **Utility Layer**: Common algorithms, data structures, I/O operations

### Design Patterns
- **Walker Pattern**: Tools traverse genomic data with apply() methods
- **Factory Pattern**: DataSourceFuncotationFactory, OutputRenderer creation
- **Strategy Pattern**: ReadFilter, VariantFilter, VariantStratifier
- **Template Method**: GATKTool defines workflow, subclasses implement specifics

### Parallelization Strategy
- **Spark RDD/DataFrame**: Distributed processing across cluster nodes
- **Sharding**: Genomic intervals divided for parallel processing
- **Broadcast Variables**: Reference data shared across executors

## Data Flow

### Variant Calling Workflow
1. **Input**: BAM/CRAM files → ReadsDataSource
2. **Filtering**: ReadFilter chain removes low-quality reads
3. **Assembly**: Active regions assembled into contigs (ReadThreadingAssembler)
4. **Alignment**: Contigs aligned to reference (Smith-Waterman)
5. **Genotyping**: Likelihood calculations → GenotypeCalculationEngine
6. **Annotation**: VariantAnnotatorEngine adds INFO/FORMAT fields
7. **Output**: VCF/GVCF via VariantContextWriter

### Structural Variant Detection Workflow
1. **Evidence Collection**: Split reads, discordant pairs, depth changes
2. **Local Assembly**: High-evidence regions assembled (FermiLiteAssembly)
3. **Contig Alignment**: BWA-MEM alignment of assembled contigs
4. **Interpretation**: ChimericAlignmentInterpreter identifies breakpoints
5. **Classification**: SvType determination (DEL, DUP, INV, BND, CPX)
6. **Genotyping**: Evidence-based genotype assignment
7. **Output**: VCF with structural variant records

### Copy Number Analysis Workflow
1. **Read Counting**: Coverage calculated per interval
2. **Normalization**: GC bias correction, sample normalization
3. **Segmentation**: KernelSegmenter identifies breakpoints
4. **Modeling**: AlleleFractionModeller + CopyRatioModeller
5. **Genotyping**: Integer copy number assignment
6. **Output**: SEG files, VCF with CNV calls

### Spark Distributed Processing
1. **Data Partitioning**: Genomic intervals split into shards
2. **Map Phase**: Each executor processes assigned shards independently
3. **Shuffle**: Intermediate results redistributed (e.g., duplicate marking)
4. **Reduce Phase**: Results aggregated (e.g., BQSR table merging)
5. **Output**: Coordinated writes to distributed filesystem (HDFS/GCS)

### Reference Data Access
- **CachingIndexedFastaSequenceFile**: On-demand reference base loading with caching
- **ReferenceMultiSparkSource**: Broadcast reference for Spark executors
- **FeatureContext**: Provides overlapping features at each locussegment data
5. **Genotyping**: Assign copy number states to segments
6. **Output**: Segmented copy number calls with quality metricsndependently
4. **Aggregation**: Results collected and merged across partitions
5. **Output**: Consolidated results written to distributed storagents format
6. Records flow to Kafka Connect framework for delivery to Kafka topics

### Incremental Snapshot Phase
1. **SignalProcessor** receives incremental snapshot signal
2. **AbstractIncrementalSnapshotChangeEventSource** chunks table data
3. Watermarks inserted into stream to track snapshot boundaries
4. Snapshot chunks interleaved with streaming events
5. **WatermarkWindowCloser** ensures consistency between snapshot and streaming data

### Schema Change Handling
1. DDL events detected in transaction log
2. **SchemaChangeEvent** created with DDL statement
3. **KafkaSchemaHistory** persists schema change to history topic
4. **DatabaseSchema** updates in-memory schema representation
5. **EventDispatcher** emits schema change event to dedicated topic

### Embedded Mode Flow
1. **AsyncEmbeddedEngine** initializes without Kafka Connect runtime
2. **EngineSourceTask** polls connector for SourceRecords
3. **ConvertingRecordCommitter** converts and commits records
4. **OffsetBackingStore** (file/memory/Kafka) persists offsets
5. Consumer receives records via callback interface