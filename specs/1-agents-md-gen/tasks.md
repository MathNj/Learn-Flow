# Tasks: Agents MD Generator

**Input**: Design documents from `/specs/1-agents-md-gen/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: This skill is test-driven. Tests are written first (Red-Green-Refactor TDD).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Skill location**: `.claude/skills/agents-md-gen/`
- **Scripts**: `.claude/skills/agents-md-gen/scripts/`
- **Tests**: `.claude/skills/agents-md-gen/tests/`
- **References**: `.claude/skills/agents-md-gen/references/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create skill directory structure at `.claude/skills/agents-md-gen/` with subdirectories: scripts/, tests/, references/
- [X] T002 Create `__init__.py` files in scripts/ and tests/ directories for Python package structure
- [X] T003 [P] Create SKILL.md with YAML frontmatter (~100 tokens) at `.claude/skills/agents-md-gen/SKILL.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core detector and pattern infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Implement language detection in `.claude/skills/agents-md-gen/scripts/detectors.py` (EXTENSION_MAP, detect_language(), detect_languages_from_files())
- [X] T005 [P] Implement framework detection in `.claude/skills/agents-md-gen/scripts/detectors.py` (FRAMEWORK_PATTERNS, parse_package_json(), parse_requirements_txt(), parse_pyproject_toml(), detect_frameworks())
- [X] T006 [P] Implement naming pattern regex and classification in `.claude/skills/agents-md-gen/scripts/patterns.py` (PATTERNS dict, classify_identifier(), detect_naming_convention())
- [X] T007 [P] Implement directory structure analysis in `.claude/skills/agents-md-gen/scripts/patterns.py` (DirectoryStructure dataclass, analyze_directory_structure(), calculate_entropy())
- [X] T008 [P] Implement safe directory walking with symlink detection in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (safe_walk(), DEFAULT_EXCLUDES, visited_inodes tracking)
- [X] T009 [P] Implement git info extraction in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (get_git_info(), get_git_remote(), get_default_branch())
- [X] T010 Implement Repository dataclass with to_markdown() method in `.claude/skills/agents-md-gen/scripts/analyze_repo.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Auto-generate Repository Documentation (Priority: P1) 🎯 MVP

**Goal**: Scan repository, detect languages, and generate AGENTS.md at repository root

**Independent Test**: Run skill against any Git repository; verify AGENTS.md is created with accurate project structure and language detection

### Tests for User Story 1 (Red Phase - Write FIRST, ensure FAIL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Unit test for language detection in `.claude/skills/agents-md-gen/tests/test_detectors.py` (test_detect_language_by_extension(), test_detect_language_by_config())
- [X] T012 [P] [US1] Unit test for framework detection in `.claude/skills/agents-md-gen/tests/test_detectors.py` (test_detect_python_frameworks(), test_detect_js_frameworks())
- [X] T013 [P] [US1] Unit test for directory walking in `.claude/skills/agents-md-gen/tests/test_analyze_repo.py` (test_safe_walk(), test_exclude_dirs(), test_symlink_detection())
- [X] T014 [P] [US1] Unit test for AGENTS.md generation in `.claude/skills/agents-md-gen/tests/test_analyze_repo.py` (test_generate_agents_md(), test_to_markdown_output())
- [X] T015 [US1] Integration test for full repository scan in `.claude/skills/agents-md-gen/tests/test_analyze_repo.py` (test_full_scan_real_repo())

### Implementation for User Story 1

- [X] T016 [US1] Implement scan_repository() function in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (orchestrates full scan, returns Repository object)
- [X] T017 [US1] Implement generate_agents_md() function in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (writes AGENTS.md to disk)
- [X] T018 [US1] Implement main() CLI entry point in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (argparse, --output, --timeout, --verbose flags)
- [X] T019 [US1] Implement AGENTS.md template rendering in Repository.to_markdown() method (Overview, Languages, Directory Structure sections)
- [X] T020 [US1] Add error handling for edge cases (no source code, permission denied, timeout) in `.claude/skills/agents-md-gen/scripts/analyze_repo.py`
- [X] T021 [US1] Verify skill runs under 30 seconds for 1,000-file repositories (add timing logging)

**Checkpoint**: At this point, User Story 1 should be fully functional - skill generates AGENTS.md with language detection and directory structure

---

## Phase 4: User Story 2 - Detect Project Conventions (Priority: P2)

**Goal**: Analyze and document coding conventions, frameworks, and patterns

**Independent Test**: Run against a repository with established patterns; verify generated documentation accurately describes conventions and frameworks

### Tests for User Story 2 (Red Phase - Write FIRST, ensure FAIL)

- [X] T022 [P] [US2] Unit test for naming convention detection in `.claude/skills/agents-md-gen/tests/test_patterns.py` (test_classify_camelcase(), test_classify_snake_case(), test_detect_dominant_convention())
- [X] T023 [P] [US2] Unit test for framework version extraction in `.claude/skills/agents-md-gen/tests/test_detectors.py` (test_extract_version_from_package_json(), test_extract_version_from_requirements())
- [X] T024 [P] [US2] Unit test for directory organization pattern detection in `.claude/skills/agents-md-gen/tests/test_patterns.py` (test_feature_based_detection(), test_type_based_detection())

### Implementation for User Story 2

- [X] T025 [P] [US2] Implement identifier extraction and sampling in `.claude/skills/agents-md-gen/scripts/patterns.py` (extract_identifiers(), sample_files())
- [X] T026 [P] [US2] Implement statistical convention analysis in `.claude/skills/agents-md-gen/scripts/patterns.py` (calculate_dominant_pattern(), confidence_threshold_check())
- [X] T027 [US2] Enhance scan_repository() to detect conventions in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (populate CodeConventions object)
- [X] T028 [US2] Enhance Repository.to_markdown() with Frameworks and Code Conventions sections in `.claude/skills/agents-md-gen/scripts/analyze_repo.py`
- [X] T029 [US2] Add test file pattern detection (e.g., *.test.ts, test_*.py) in `.claude/skills/agents-md-gen/scripts/patterns.py`

**Checkpoint**: User Stories 1 AND 2 should both work - AGENTS.md now includes languages, frameworks, conventions, and test patterns

---

## Phase 5: User Story 3 - Customizable Output Sections (Priority: P3)

**Goal**: Allow users to specify which sections to include in generated AGENTS.md

**Independent Test**: Run with custom section flags; verify only requested sections appear in output

### Tests for User Story 3 (Red Phase - Write FIRST, ensure FAIL)

- [X] T030 [P] [US3] Unit test for section filtering in `.claude/skills/agents-md-gen/tests/test_analyze_repo.py` (test_filter_sections(), test_sections_languages_only(), test_sections_frameworks_only())
- [X] T031 [P] [US3] Unit test for --check-only mode in `.claude/skills/agents-md-gen/tests/test_analyze_repo.py` (test_check_only_no_change(), test_check_only_with_change())

### Implementation for User Story 3

- [X] T032 [US3] Implement section filtering logic in `.claude/skills/agents-md-gen/scripts/analyze_repo.py` (parse_sections_arg(), filter_sections(), conditional rendering)
- [X] T033 [US3] Add --sections CLI argument in `.claude/skills/agents-md-gen/scripts/analyze_repo.py`
- [X] T034 [US3] Implement --check-only mode (compare existing AGENTS.md, exit 1 if different) in `.claude/skills/agents-md-gen/scripts/analyze_repo.py`
- [X] T035 [US3] Add --no-git flag to skip git information gathering in `.claude/skills/agents-md-gen/scripts/analyze_repo.py`

**Checkpoint**: All user stories complete - skill supports full AGENTS.md generation with customizable sections

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T036 [P] Create reference documentation in `.claude/skills/agents-md-gen/references/agents_spec.md` (Agent Skills specification summary)
- [X] T037 [P] Create reference documentation in `.claude/skills/agents-md-gen/references/framework_patterns.md` (Known framework detection patterns)
- [X] T038 Run pytest with coverage and ensure >80% code coverage in `.claude/skills/agents-md-gen/tests/`
- [X] T039 Validate token efficiency: SKILL.md should be <100 tokens in `.claude/skills/agents-md-gen/SKILL.md`
- [X] T040 Test skill on real repositories (Python, JavaScript, mixed) and validate output quality
- [X] T041 Add --help documentation and validate all CLI options are documented
- [X] T042 Run quickstart.md validation - verify all examples work as documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Modifies output format, independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Red-Green-Refactor)
- Detection functions before main orchestration
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Foundational tasks T004-T009 marked [P] can run in parallel (different files)
- All tests within a story marked [P] can run in parallel
- Once Foundational phase completes, US1, US2, US3 can be worked on in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational detection tasks in parallel:
Task: "Implement language detection in scripts/detectors.py"
Task: "Implement framework detection in scripts/detectors.py"
Task: "Implement naming pattern regex in scripts/patterns.py"
Task: "Implement directory structure analysis in scripts/patterns.py"
Task: "Implement safe directory walking in scripts/analyze_repo.py"
Task: "Implement git info extraction in scripts/analyze_repo.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T010) - CRITICAL
3. Complete Phase 3: User Story 1 (T011-T021)
4. **STOP and VALIDATE**: Test against real repository, verify AGENTS.md generation
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP complete!
3. Add User Story 2 → Test independently → Conventions detected
4. Add User Story 3 → Test independently → Customizable output
5. Polish → Production-ready skill

### Test-Driven Development (Red-Green-Refactor)

For each user story:
1. **Red**: Write tests, verify they FAIL
2. **Green**: Write minimal code to pass tests
3. **Refactor**: Clean up while keeping tests green

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3] labels map task to specific user story
- Each user story is independently testable and deliverable
- Verify tests fail before implementing (TDD Red phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- SKILL.md target: ~100 tokens (progressive disclosure)
- Token efficiency: Script executes outside context, returns only AGENTS.md content (~500 tokens vs 50,000+ for full repo)
