# Framework Detection Patterns Reference

## Overview

This document catalogs the known framework detection patterns used by the agents-md-gen skill. These patterns are used to identify frameworks and libraries from project configuration files.

## Detection Method

1. **Config File Detection**: Identify language-specific configuration files
2. **Dependency Parsing**: Extract package names and versions
3. **Pattern Matching**: Match dependency names against known framework patterns

## Language-Specific Patterns

### Python

**Config Files**: `requirements.txt`, `pyproject.toml`, `setup.py`

| Dependency Name | Framework | Category | Version Source |
|-----------------|-----------|----------|-----------------|
| `django` | Django | api | requirements.txt |
| `fastapi` | FastAPI | api | requirements.txt |
| `flask` | Flask | api | requirements.txt |
| `pytest` | pytest | testing | requirements.txt |
| `black` | black | build | requirements.txt |
| `mypy` | mypy | build | requirements.txt |

**Version Extraction Patterns:**
- `package==version` → exact version
- `package>=version` → minimum version
- `package~=version` → compatible release

### JavaScript/TypeScript

**Config Files**: `package.json`

| Dependency Name | Framework | Category | Location |
|-----------------|-----------|----------|----------|
| `next` | Next.js | web | dependencies |
| `nuxt` | Nuxt.js | web | dependencies |
| `react` | React | web | dependencies |
| `vue` | Vue.js | web | dependencies |
| `svelte` | Svelte | web | dependencies |
| `angular` | Angular | web | dependencies |
| `express` | Express | api | dependencies |
| `jest` | Jest | testing | devDependencies |
| `vitest` | Vitest | testing | devDependencies |
| `webpack` | webpack | build | devDependencies |
| `vite` | Vite | build | devDependencies |
| `typescript` | TypeScript | build | devDependencies |

**Version Parsing**: Direct value from package.json

### Java

**Config Files**: `pom.xml` (Maven), `build.gradle` (Gradle)

| Pattern | Framework | Category | Detection Method |
|---------|-----------|----------|------------------|
| `spring-boot-starter-parent` (parent POM) | Spring Boot | api | Parent groupId/artifactId |
| `spring-boot-starter-*` (dependency) | Spring Boot | api | Dependency artifactId |
| `org.springframework.boot` (plugin) | Spring Boot | api | Plugin groupId |

**Version Source**: Parent POM version or dependency version

### Ruby

**Config Files**: `Gemfile`

| Gem Name | Framework | Category | Version Source |
|----------|-----------|----------|-----------------|
| `rails` | Rails | api | Gemfile |
| `railties` | Rails | api | Gemfile |
| `rspec` | RSpec | testing | Gemfile |

**Version Extraction**: Regex from `gem "name", "version"` pattern

### Go

**Config Files**: `go.mod`

| Module Path | Framework | Category |
|-------------|-----------|----------|
| (Standard library only) | Go stdlib | api |

**Note**: Go framework detection is limited as most frameworks are imported via module paths rather than declared in go.mod.

### Rust

**Config Files**: `Cargo.toml`

| Crate Name | Framework | Category |
|------------|-----------|----------|
| (Standard library only) | Rust stdlib | api |

**Note**: Rust framework detection follows similar limitations as Go.

## Detection Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `web` | Frontend frameworks | React, Vue, Next.js, Angular |
| `api` | Backend frameworks | Django, FastAPI, Express, Spring Boot |
| `testing` | Test frameworks | pytest, Jest, RSpec |
| `build` | Build tools | webpack, Vite, black, mypy |

## Adding New Patterns

To add a new framework detection pattern:

1. **Determine the language** and config file format
2. **Add to `FRAMEWORK_PATTERNS`** in `scripts/detectors.py`
3. **Create parser function** if config file format is new
4. **Add tests** in `tests/test_detectors.py`

**Example:**
```python
# In FRAMEWORK_PATTERNS
"Python": {
    "requirements.txt": {
        "new-framework": "NewFramework",
    },
},
```

## Version Extraction Examples

### requirements.txt
```
django==4.2.0          → version: "4.2"
fastapi>=0.104.0       → version: "0.104.0"
pytest~=7.4            → version: "7"
```

### package.json
```json
{
  "dependencies": {
    "next": "14.0.0",
    "react": "^18.0"
  }
}
```
→ Next.js version: "14.0", React version: "18.0"

### pom.xml
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.0.0</version>
</parent>
```
→ Spring Boot version: "3.0.0"

### Gemfile
```ruby
gem "rails", "~> 7.0"
gem "rspec", "~> 3.0"
```
→ Rails version: "7.0", RSpec version: "3.0"

## Confidence Levels

| Confidence | Meaning |
|------------|---------|
| 1.0 | Exact match on dependency name |
| 0.8-0.9 | Partial match or common alias |
| <0.8 | Tentative detection |

## References

- [Python Packaging Index](https://pypi.org/)
- [npm Registry](https://www.npmjs.com/)
- [Maven Central](https://mvnrepository.com/)
- [RubyGems](https://rubygems.org/)
