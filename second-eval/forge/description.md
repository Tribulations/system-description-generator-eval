# Forge Game System - High-Level Overview

## System Purpose
Forge is a Java-based implementation of a trading card game engine (Magic: The Gathering). The system manages game state, card mechanics, player interactions, spell resolution, and combat logic for digital card game matches.

## Key Components & Responsibilities

### 1. **Card (forge.game.card)**
- **Core game object** representing individual cards in play, hand, graveyard, and other zones
- Manages card state (tapped/untapped, face up/down, transformed, mutated)
- Tracks power/toughness, counters, damage, and keywords
- Handles card type changes, color changes, and text modifications
- Maintains relationships (attached cards, paired cards, merged cards)
- Provides view synchronization for UI updates through extensive `updateXForView()` methods

### 2. **Player (forge.game.player)**
- Represents each game participant
- Manages life totals, poison counters, energy counters, and mana shards
- Tracks game statistics (cards drawn, spells cast, lands played)
- Handles zone access (hand, library, graveyard, battlefield, exile)
- Manages player-specific game states (monarch, initiative, ring bearer)
- Controls team relationships and opponent identification
- Enforces game rules (maximum hand size, drawing restrictions)

### 3. **SpellAbility (forge.game.spellability)**
- Represents activated abilities, triggered abilities, and spells
- Manages targeting, costs, and resolution
- Handles mana abilities and non-mana abilities
- Tracks ability restrictions and conditions
- Supports alternative costs (kicker, flashback, emerge, bestow)
- Maintains parent-child relationships for sub-abilities
- Provides stack description generation for game log

### 4. **SpellAbilityEffect (forge.game.ability)**
- Executes the actual effects of spells and abilities
- Processes game actions when abilities resolve
- Interfaces with replacement effects and triggers

## Core Technologies & Dependencies

### Language & Platform
- **Java** (primary implementation language)
- Uses Java collections framework extensively

### Key Libraries
- **Apache Commons Lang3** - String utilities, tuple support, mutable objects
- **Google Guava** - Enhanced collections (Multimap, Table, Iterables, Lists)
- **Esotericsoftware MinLog** - Logging framework
- **Sentry** - Error tracking and monitoring

### Internal Dependencies
- **forge.card** - Card database, card types, mana costs, rarity
- **forge.game.zone** - Zone management (battlefield, hand, library, etc.)
- **forge.game.trigger** - Triggered ability system
- **forge.game.replacement** - Replacement effect system
- **forge.game.staticability** - Static ability system
- **forge.game.keyword** - Keyword ability handling
- **forge.game.cost** - Cost payment system
- **forge.game.mana** - Mana pool and mana cost management
- **forge.game.combat** - Combat phase handling
- **forge.game.event** - Event system for game actions
- **forge.trackable** - View synchronization framework

## Architecture

### Design Pattern: **Model-View Architecture**
- **Model Layer**: Game objects (Card, Player, SpellAbility) maintain authoritative game state
- **View Layer**: Separate view classes (CardView, PlayerView, SpellAbilityView) provide read-only snapshots for UI
- **Synchronization**: Extensive `updateXForView()` methods propagate state changes to views

### Component Organization
- **Game State Management**: Centralized in Game class, distributed across Card and Player objects
- **Rule Enforcement**: Distributed through static abilities, replacement effects, and condition checks
- **Effect Resolution**: Handled by SpellAbilityEffect and ability-specific effect classes
- **Event System**: Observer pattern for triggers and state-dependent actions

### Key Architectural Features
- **Layered Timestamps**: Cards and effects track multiple timestamps (game, layer, transform) for dependency ordering
- **Zone-Based State**: Card behavior varies based on current zone (battlefield, hand, graveyard, etc.)
- **Ability Hierarchy**: SpellAbility supports parent-child relationships for complex multi-step effects
- **Keyword System**: Extensible keyword interface for card mechanics

## Data Flow

### 1. **Card State Changes**
```
User Action → SpellAbility → SpellAbilityEffect → Card.setState() → Card.updateXForView() → CardView → UI
```

### 2. **Spell/Ability Resolution**
```
Player activates ability → SpellAbility.resolve() → SpellAbilityEffect.resolve() → 
Game state modification → Trigger checks → Replacement effect checks → Event firing → View updates
```

### 3. **Combat Flow**
```
Declare attackers → Card.updateAttackingForView() → Combat object creation →
Declare blockers → Card.updateBlockingForView() → Damage assignment → 
Card.setDamage() → Lethal damage checks → State-based actions
```

### 4. **Targeting Flow**
```
SpellAbility.usesTargeting() → TargetRestrictions validation → 
TargetChoices population → SpellAbility.resolve() → Effect applies to targets
```

### 5. **Mana Payment**
```
Cost.getPayCosts() → ManaCostBeingPaid → ManaPool.payManaFrom() → 
SpellAbility.setPayingMana() → Mana tracking for color identity/restrictions
```

### 6. **View Synchronization**
```
Game state change → updateXForView() method → TrackableProperty modification → 
View object update → UI refresh (via observer pattern)
```

### 7. **Keyword Processing**
```
Card.getKeywords() → KeywordInterface collection → Static ability application →
Changed keyword tracking → Keyword effect enforcement during game actions
```

This system implements a comprehensive rules engine with extensive state tracking, effect layering, and view synchronization to support complex card game mechanics in a digital environment.
