# Manual Study: RuneLite

## System Purpose

RuneLite is a free, open source client for the MMO game OldSchool RuneScape (OSRS) allowing users with additional functionalities which does not exist in the original game. RuneLite interacts with the OSRS servers as an additional layer for its users. 

## Architectural Approach
- modular approach with separate plugins for adding features
- dependency injection with guice
- Annotation-driven configuration
- uses mvc principles

## Key Modules and Components

- cache (caches game data)
- client (Primary module containing the core RuneLite client)
- runelite-api (Defines the public interfaces, event structures, and data models for interaction with the RuneLite client)
- jshell (integrates a jshell environment for live debugging, scripting etc.)
- runelite-maven-plugin (custom maven plugin for automating build tasks)

## Notable Design Patterns and Techniques

- SLFJ and logback for logging
- observer pattern (Event bus)
- partially mvc
- plugin architecture

## Relationships and Dependencies

The abstract Plugin class extends Module class. The Plugin class is in turn extended by all concrete "plugin classes".

## Important Implementation Details
Uses Lombok but it is not mentioned in the generated description (GD)
GD does not mention the Plugin Hub which is a feature that maybe should be mentioned for improved high level understanding.
RuneLite is heavily Plugin based. Should have been mentioned more explicitly in GD?
Other repo in the RuneLite ecosystem (or not as RuneLite devs does not support them?): https://github.com/runelite/plugin-hub 

## References
https://github.com/runelite/runelite/wiki/Developer-Guide
https://static.runelite.net/runelite-api/apidocs/
https://static.runelite.net/runelite-client/apidocs/
https://github.com/runelite/runelite/wiki/Building-with-IntelliJ-IDEA

[**Back to:** Manual Evaluation Guide](manual_evaluation_guide.md)
