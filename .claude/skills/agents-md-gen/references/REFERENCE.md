# AGENTS.md Generator - Reference

Complete reference for the AGENTS.md generation skill.

## Template Customization

The generator uses a template-based approach. Customize the output by modifying the template section in `generate.py`.

### Template Sections

| Section | Description |
|---------|-------------|
| Project Overview | Auto-detected from repository name |
| Technology Stack | Detected languages and frameworks |
| Directory Structure | Simplified tree view |
| Development Commands | Placeholder for user to fill |
| Conventions | Placeholder for user to fill |

## Framework Detection Patterns

### Python Projects

Detects:
- `requirements.txt` → pip
- `setup.py` → setuptools
- `pyproject.toml` → poetry or setuptools
- `poetry.lock` → poetry
- `Pipfile` → pipenv

### Node.js Projects

Detects:
- `package.json` → npm/yarn/pnpm
- `yarn.lock` → yarn
- `pnpm-lock.yaml` → pnpm
- `tsconfig.json` → TypeScript
- `next.config.js` → Next.js

### Java Projects

Detects:
- `pom.xml` → Maven
- `build.gradle` / `build.gradle.kts` → Gradle
- `gradlew` → Gradle wrapper

### Go Projects

Detects:
- `go.mod` → Go modules
- `go.sum` → Go modules

### Rust Projects

Detects:
- `Cargo.toml` → Cargo
- `Cargo.lock` → Cargo

## Advanced Configuration

### Custom Detection Rules

Add new language or framework detection in `generate.py`:

```python
# Add to LANGUAGE_MAP
'.xyz': 'XyzLanguage',

# Add to FRAMEWORK_INDICATORS
'my-config.json': 'MyFramework',
```

### Custom Output Format

Modify the `generate_agents_md()` function to change output format.

### Excluding Directories

Add directories to the exclude list:

```python
dirs[:] = [d for d in dirs if d not in {
    '.git', '.idea', 'node_modules',
    'my-custom-dir',  # Add your exclusions here
}]
```

## Script Options

```
usage: generate.py [-h] [--path PATH] [--output OUTPUT] [--verbose]

Generate AGENTS.md for a codebase

optional arguments:
  -h, --help       show this help message and exit
  --path PATH      Path to the repository (default: .)
  --output OUTPUT  Output file path (default: AGENTS.md in repo root)
  --verbose, -v    Show detailed output
```

## Examples

### Generate for current directory
```bash
python scripts/generate.py
```

### Generate for specific path
```bash
python scripts/generate.py --path /path/to/repo
```

### Generate to custom output
```bash
python scripts/generate.py --output /tmp/AGENTS.md
```

### Verbose output
```bash
python scripts/generate.py --verbose
```

## Troubleshooting

### No languages detected
- Ensure source files have recognized extensions
- Check that source directories aren't excluded

### Empty directory structure
- Verify repository has files
- Check read permissions

### Encoding errors
- Ensure files use UTF-8 encoding
- Check for binary files being scanned

## Best Practices

1. **Run after significant changes**: Regenerate AGENTS.md when structure changes
2. **Customize the placeholders**: Fill in development commands and conventions
3. **Keep in repo root**: AGENTS.md should be at the repository root
4. **Commit with code**: Update AGENTS.md along with code changes
