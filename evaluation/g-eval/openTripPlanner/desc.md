System Description: Here's a structured high-level summary of the OpenTripPlanner system:

**1. System Purpose**
OpenTripPlanner is a transit routing engine that provides multi-modal trip planning services, calculating routes that can combine public transit, walking, cycling, and other transportation modes.

**2. Key Components & Responsibilities**

- **Builder Class**
  - Handles configuration and construction of routing parameters
  - Manages transit preferences, costs, and optimization settings
  - Implements builder patterns for creating routing requests

- **DefaultTransitService**
  - Provides core transit data access and management
  - Handles scheduling, route finding, and stop location services
  - Manages real-time transit updates and service patterns

- **GraphQLQueryTypePlanArgs**
  - Manages GraphQL query parameters for trip planning
  - Handles user input validation and parameter processing
  - Supports various routing preferences and constraints

**3. Core Technologies & Dependencies**

Primary Technologies:
- Java (primary programming language)
- GraphQL (API query language)
- Raptor Algorithm (for transit routing)

Key Dependencies:
- Jakarta Inject (dependency injection)
- JTS Topology Suite (geometric operations)
- Collection frameworks (Java utilities)
- Time/Date handling libraries
- Spatial data processing utilities

The system is built using modern Java practices, employing builder patterns, dependency injection, and service-oriented architecture to provide flexible and efficient transit routing capabilities. It integrates real-time updates and supports multiple transportation modes while offering GraphQL-based API access to its functionality.