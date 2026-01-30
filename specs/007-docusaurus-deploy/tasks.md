# Tasks: Docusaurus Documentation Deployment

**Input**: Design documents from `/specs/007-docusaurus-deploy/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Build validation, link checking, Lighthouse CI for performance testing

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

All paths are relative to repository root. The documentation site will be created in the `documentation/` directory.

```text
documentation/
├── docusaurus.config.ts    # Main TypeScript configuration
├── sidebars.ts             # Sidebar navigation configuration
├── tsconfig.json           # TypeScript compiler options
├── package.json            # Dependencies and scripts
├── src/
│   ├── css/
│   │   └── custom.css      # Custom styles/branding
│   └── components/         # Custom React components (OPTIONAL)
├── docs/                   # Documentation markdown files
│   ├── getting-started/
│   ├── skills-library/
│   ├── architecture/
│   ├── api/
│   ├── deployment/
│   └── platform/
├── static/                 # Static assets
│   └── img/
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## Phase 0: Project Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure

**Acceptance**: Docusaurus project initialized, TypeScript configured, development server runs successfully

- [ ] **T001** Create `documentation/` directory structure at repository root
- [ ] **T002** Initialize Docusaurus with TypeScript using `npx create-docusaurus@latest . --typescript`
- [ ] **T003** [P] Install `@docusaurus/theme-mermaid` for Mermaid diagram support
- [ ] **T004** [P] Install `@easyops-cn/docusaurus-search-local` for built-in search fallback
- [ ] **T005** Configure `tsconfig.json` with strict mode and path aliases (`@site/*` → `./`)
- [ ] **T006** Update `package.json` scripts: `start`, `build`, `serve`, `swizzle`
- [ ] **T007** Verify development server starts at localhost:3000 with `npm run start`

**Checkpoint**: Docusaurus TypeScript project initialized and running locally

---

## Phase 1: User Story 1 - Documentation Site Initialization (Priority: P1) 🎯 MVP

**Goal**: Initialize Docusaurus with TypeScript and verify the site builds and runs locally

**Independent Test**: Run `npm run start` and verify the default Docusaurus welcome page loads at localhost:3000. Run `npm run build` and verify the `build/` directory contains static HTML files.

**Functional Requirements**: FR-001 (TypeScript config), FR-004 (Static site build)

### Implementation for US1

- [ ] **T008** [P] [US1] Create `documentation/docusaurus.config.ts` with basic TypeScript configuration
  - Set `title`, `url`, `baseUrl`
  - Configure `@docusaurus/preset-classic`
  - Set `markdown.mermaid: true`
  - Set `onBrokenLinks: 'throw'` and `onBrokenMarkdownLinks: 'warn'`

- [ ] **T009** [US1] Create `documentation/sidebars.ts` with TypeScript type definitions
  - Import `SidebarsConfig` type from `@docusaurus/plugin-content-docs`
  - Define empty sidebar structure (will populate in US2)

- [ ] **T010** [P] [US1] Create `documentation/src/css/custom.css` with base styles
  - Import Docusaurus variables
  - Add placeholder for custom branding styles

- [ ] **T011** [US1] Create placeholder `documentation/docs/intro.md` with frontmatter
  ```yaml
  ---
  id: intro
  title: Introduction
  ---
  ```

- [ ] **T012** [US1] Run `npm run build` and verify static site generation
  - Confirm `build/` directory created
  - Verify `index.html` exists
  - Check for `assets/js/` and `assets/css/` directories

- [ ] **T013** [US1] Test `npm run serve` and preview production build locally

**Checkpoint**: US1 complete - Docusaurus site initializes, builds, and serves static HTML. MVP foundation ready.

---

## Phase 2: User Story 5 - Static Site Deployment (Priority: P1) 🎯 MVP

**Goal**: Configure GitHub Actions deployment to GitHub Pages

**Independent Test**: Push to main branch and verify documentation deploys to GitHub Pages URL. Confirm site is publicly accessible.

**Functional Requirements**: FR-004 (Static site build), FR-005 (Deployment to static hosting)

### Implementation for US5

- [ ] **T014** [P] [US5] Create `documentation/.github/workflows/deploy.yml` GitHub Actions workflow
  - Trigger on push to `main` branch
  - Set up Node.js 20
  - Run `npm ci` and `npm run build`
  - Configure GitHub Pages deployment
  - Use `actions/upload-pages-artifact@v3` and `actions/deploy-pages@v4`

- [ ] **T015** [P] [US5] Create `documentation/netlify.toml` as alternative deployment config
  - Set build command to `npm run build`
  - Set publish directory to `build`
  - Set `NODE_VERSION = "20"`

- [ ] **T016** [P] [US5] Create `documentation/vercel.json` as alternative deployment config
  - Set `buildCommand: "npm run build"`
  - Set `outputDirectory: "build"`

- [ ] **T017** [US5] Configure `documentation/docusaurus.config.ts` with deployment settings
  - Set `organizationName` to GitHub org/user
  - Set `projectName` to repository name
  - Set `deploymentBranch` to `gh-pages`
  - Configure `baseUrl` for GitHub Pages (usually `/` or `/repo-name/`)

- [ ] **T018** [US5] Test deployment to GitHub Pages
  - Push changes to `main` branch
  - Monitor GitHub Actions workflow
  - Verify deployment succeeds
  - Confirm site accessible at GitHub Pages URL

- [ ] **T019** [US5] Validate link checking in CI build
  - Add `--fail-on-broken-links` flag to build command in GitHub Actions
  - Test with intentional broken link to verify detection

**Checkpoint**: US5 complete - Documentation deploys to GitHub Pages automatically on push. Site publicly accessible.

---

## Phase 3: User Story 2 - Branding and Navigation Configuration (Priority: P2)

**Goal**: Apply LearnFlow branding (title, logo, colors) and configure sidebar navigation for all 6 sections

**Independent Test**: Verify site displays LearnFlow title, logo (if provided), and custom colors. Confirm sidebar shows all 6 sections with correct hierarchy.

**Functional Requirements**: FR-002 (Branding), FR-007 (Sidebar navigation)

### Implementation for US2

- [ ] **T020** [P] [US2] Update `documentation/docusaurus.config.ts` with LearnFlow branding
  - Set `title: "LearnFlow Documentation"`
  - Set `tagline: "AI-Powered Learning Platform"`
  - Configure `favicon` path in `static/img/`

- [ ] **T021** [P] [US2] Configure navbar in `documentation/docusaurus.config.ts`
  - Add Docs link to left side
  - Add GitHub repository link to right side
  - Add search placeholder to right side

- [ ] **T022** [P] [US2] Configure footer in `documentation/docusaurus.config.ts`
  - Add Docs section with links to Getting Started, API
  - Add Community section with links to GitHub, Discord
  - Add copyright with current year

- [ ] **T023** [US2] Update `documentation/src/css/custom.css` with LearnFlow brand colors
  - Define CSS custom properties for primary colors
  - Override `--ifm-color-primary` and `--ifm-color-primary-dark`
  - Add custom logo styling (if logo provided)

- [ ] **T024** [US2] Create `documentation/sidebars.ts` with full 6-section structure
  - Define `docsSidebar` with categories: Getting Started, Skills Library, Architecture, API Documentation, Deployment, LearnFlow Platform
  - Use category type for sections, doc type for individual pages

- [ ] **T025** [P] [US2] Create `documentation/docs/getting-started/` directory and markdown files
  - `installation.md` with frontmatter (id, title, description)
  - `quick-start.md` with frontmatter
  - `configuration.md` with frontmatter

- [ ] **T026** [P] [US2] Create `documentation/docs/skills-library/` directory and markdown files
  - `overview.md` with frontmatter
  - `development.md` with frontmatter
  - `reference.md` with frontmatter

- [ ] **T027** [P] [US2] Create `documentation/docs/architecture/` directory and markdown files
  - `system-overview.md` with frontmatter
  - `microservices.md` with frontmatter
  - `event-flow.md` with frontmatter

- [ ] **T028** [P] [US2] Create `documentation/docs/api/` directory and markdown files
  - `rest.md` with frontmatter
  - `kafka-topics.md` with frontmatter
  - `websocket.md` with frontmatter

- [ ] **T029** [P] [US2] Create `documentation/docs/deployment/` directory and markdown files
  - `kubernetes.md` with frontmatter
  - `cloud-platforms.md` with frontmatter
  - `ci-cd.md` with frontmatter
  - `troubleshooting.md` with frontmatter

- [ ] **T030** [P] [US2] Create `documentation/docs/platform/` directory and markdown files
  - `user-guide.md` with frontmatter
  - `teacher-guide.md` with frontmatter
  - `student-guide.md` with frontmatter

- [ ] **T031** [US2] Add placeholder content to each markdown file with section headers and example content

- [ ] **T032** [US2] Run `npm run build` and verify sidebar renders correctly
  - Check all 6 categories appear
  - Verify nested items display correctly
  - Test collapsible categories

**Checkpoint**: US2 complete - Site branded with LearnFlow identity. Sidebar navigation shows all 6 sections.

---

## Phase 4: User Story 3 - Content Authoring with Enhanced Features (Priority: P2)

**Goal**: Enable syntax highlighting, Mermaid diagrams, and link validation for documentation content

**Independent Test**: Create markdown with code blocks, Mermaid diagram, and links. Build and verify code highlights, diagram renders, and broken links are detected.

**Functional Requirements**: FR-003 (Markdown to HTML), FR-008 (Syntax highlighting), FR-009 (Link validation), FR-010 (Mermaid diagrams)

### Implementation for US3

- [ ] **T033** [P] [US3] Configure prism-react-renderer in `documentation/docusaurus.config.ts`
  - Import `themes` from `prism-react-renderer`
  - Set `theme: themes.github` for light mode
  - Set `darkTheme: themes.dracula` for dark mode
  - Add `additionalLanguages: ['python', 'java', 'typescript', 'yaml', 'bash', 'javascript']`

- [ ] **T034** [US3] Enable Mermaid theme in `documentation/docusaurus.config.ts`
  - Add `mermaid.theme` configuration
  - Set light theme to `neutral`
  - Set dark theme to `dark`

- [ ] **T035** [US3] Add `@docusaurus/theme-mermaid` to themes array in `documentation/docusaurus.config.ts`
  - Ensure `markdown.mermaid: true` is set
  - Verify theme loads correctly

- [ ] **T036** [P] [US3] Create example page with code blocks at `documentation/docs/getting-started/quick-start.md`
  - Add Python code block with syntax highlighting
  - Add TypeScript code block with syntax highlighting
  - Add YAML configuration example

- [ ] **T037** [P] [US3] Add Mermaid diagram examples to documentation
  - Add flowchart diagram to `architecture/system-overview.md`
  - Add sequence diagram to `architecture/event-flow.md`
  - Add class diagram to `skills-library/overview.md`

- [ ] **T038** [US3] Test link validation by creating intentional broken link
  - Add broken internal link to a page
  - Run `npm run build` and verify error is thrown
  - Fix broken link and verify build succeeds

- [ ] **T039** [US3] Add internal links between documentation pages
  - Link from `installation.md` to `quick-start.md`
  - Link from `architecture/` pages to `api/` pages
  - Use relative paths with `.md` extension

- [ ] **T040** [US3] Run `npm run build` with `--fail-on-broken-links` flag
  - Verify all internal links validate
  - Confirm no broken links in build output
  - Check build time is under 5 minutes (SC-002)

**Checkpoint**: US3 complete - Code highlighting works, Mermaid diagrams render, links validate during build.

---

## Phase 5: User Story 4 - Search Functionality (Priority: P3)

**Goal**: Configure search functionality using Algolia DocSearch or built-in search fallback

**Independent Test**: Type a query in the search box and verify results appear. For built-in search, verify results appear without external API calls.

**Functional Requirements**: FR-006 (Search configuration)

### Implementation for US4

- [ ] **T041** [P] [US4] Apply for Algolia DocSearch at https://docsearch.algolia.com/apply (manual step)
  - Submit documentation URL
  - Wait for approval email (can take days)
  - Document credentials securely

- [ ] **T042** [US4] Configure built-in search as fallback in `documentation/docusaurus.config.ts`
  - Add `@easyops-cn/docusaurus-search-local` to themes array
  - Configure with `hashed: true` for performance
  - Set `language: ['en']`

- [ ] **T043** [US4] Add Algolia configuration placeholder in `documentation/docusaurus.config.ts`
  - Create `algolia` object in `themeConfig`
  - Add placeholder comments for `appId`, `apiKey`, `indexName`
  - Note: Only populate after Algolia approval

- [ ] **T044** [US4] Test built-in search functionality
  - Run `npm run start`
  - Type query in search box
  - Verify results appear from documentation content
  - Confirm search response time <500ms (SC-005)

- [ ] **T045** [US4] If Algolia approved, update `documentation/docusaurus.config.ts` with credentials
  - Add `appId` from Algolia
  - Add `apiKey` (search-only key)
  - Add `indexName`
  - Test search on deployed site

- [ ] **T046** [US4] Document search configuration in `documentation/docs/getting-started/configuration.md`
  - Explain built-in search vs Algolia
  - Provide instructions for switching providers
  - Include common search issues and solutions

**Checkpoint**: US4 complete - Search functionality works. Built-in search operational, Algolia ready when approved.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, validation, and documentation

- [ ] **T047** [P] Add branding assets to `documentation/static/img/`
  - Add `logo.svg` (or use placeholder)
  - Add `favicon.ico` (or use Docusaurus default)
  - Add `og-image.png` for social sharing

- [ ] **T048** [P] Create `README.md` in documentation root with setup instructions
  - Document prerequisites (Node.js 20+)
  - Include quick start commands
  - Link to full quickstart guide

- [ ] **T049** Run Lighthouse CI test and verify scores ≥90 (SC-007)
  - Install `lhci` CLI or use Chrome DevTools
  - Run Lighthouse on deployed site
  - Verify Performance ≥90
  - Verify Accessibility ≥90
  - Verify Best Practices ≥90
  - Verify SEO ≥90

- [ ] **T050** Optimize images in `documentation/static/img/`
  - Convert to WebP format where supported
  - Ensure images are compressed
  - Add width/height attributes to prevent layout shift

- [ ] **T051** Add `robots.txt` to `documentation/static/` for SEO
  - Allow all crawlers
  - Add sitemap reference

- [ ] **T052** [P] Update documentation content with actual LearnFlow information
  - Replace placeholder content with real docs
  - Add code examples relevant to LearnFlow
  - Include actual architecture diagrams

- [ ] **T053** Test navigation depth - verify any page reachable in 3 clicks (SC-004)
  - Test deepest nested pages
  - Count clicks from home
  - Adjust sidebar structure if needed

- [ ] **T054** Validate initialization time is under 2 minutes (SC-001)
  - Fresh clone of repository
  - Time `npm install` and `npm run build`
  - Should complete in <120 seconds

- [ ] **T055** [P] Create deployment documentation for Netlify/Vercel alternatives
  - Document Netlify deployment steps
  - Document Vercel deployment steps
  - Include configuration file references

**Checkpoint**: All polish tasks complete. Documentation site production-ready.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 0 (Setup)**: No dependencies - can start immediately
- **Phase 1 (US1)**: Depends on Phase 0 completion - BLOCKS all other phases
- **Phase 2 (US5)**: Depends on Phase 1 completion - can run parallel to US2/US3
- **Phase 3 (US2)**: Depends on Phase 1 completion - can run parallel to US3/US5
- **Phase 4 (US3)**: Depends on Phase 1 completion - can run parallel to US2/US5
- **Phase 5 (US4)**: Depends on Phase 1 completion - independent of US2/US3/US5
- **Phase 6 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

| User Story | Depends On | Can Run Parallel With |
|------------|------------|----------------------|
| US1: Site Initialization | Phase 0 only | None (must complete first) |
| US2: Branding & Navigation | US1 | US3, US4, US5 |
| US3: Content Features | US1 | US2, US4, US5 |
| US4: Search | US1 | US2, US3, US5 |
| US5: Deployment | US1 | US2, US3, US4 |

### Parallel Opportunities

**Within Phase 0 (Setup)**:
- T003, T004 can run in parallel (different npm packages)

**Within Phase 1 (US1)**:
- T008, T009, T010 can run in parallel (different files)

**Within Phase 3 (US2)**:
- T025-T030 can all run in parallel (different directories)

**Within Phase 4 (US3)**:
- T036, T037 can run in parallel (different pages)

**Across User Stories** (after US1 completes):
- US2, US3, US4, US5 can all proceed in parallel if team capacity allows

---

## Implementation Strategy

### MVP First (US1 + US5 Only)

1. Complete Phase 0: Setup (T001-T007)
2. Complete Phase 1: US1 Site Initialization (T008-T013)
3. Complete Phase 2: US5 Deployment (T014-T019)
4. **STOP and VALIDATE**: Test deployed documentation site
5. Deploy/demo if ready

**Deliverable**: Working documentation site deployed to GitHub Pages with basic branding

### Incremental Delivery

1. **Foundation** (Phase 0 + US1): Docusaurus initialized and building
2. **Add Deployment** (US5): Auto-deployment to GitHub Pages → MVP Complete
3. **Add Branding** (US2): LearnFlow branding, full sidebar structure
4. **Add Features** (US3): Syntax highlighting, Mermaid diagrams, link validation
5. **Add Search** (US4): Built-in search ready, Algolia configured when approved
6. **Polish** (Phase 6): Performance optimization, final validation

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Phase 0 (Setup) together
2. Once US1 (Site Initialization) is done:
   - **Developer A**: US2 (Branding & Navigation) - T020-T032
   - **Developer B**: US3 (Content Features) - T033-T040
   - **Developer C**: US5 (Deployment) - T014-T019
3. After US2/US3/US5 complete:
   - **Developer A**: US4 (Search) - T041-T046
4. Team completes Phase 6 (Polish) together

---

## Task Summary by Functional Requirement

| FR | Description | Tasks |
|----|-------------|-------|
| FR-001 | TypeScript config | T002, T005, T008, T009 |
| FR-002 | Branding config | T020-T024, T047 |
| FR-003 | Markdown to HTML | T011, T031, T036, T037 |
| FR-004 | Static site build | T006, T012, T013, T040 |
| FR-005 | Deployment support | T014-T019 |
| FR-006 | Search configuration | T004, T041-T046 |
| FR-007 | Sidebar navigation | T009, T024, T025-T030, T032 |
| FR-008 | Syntax highlighting | T033, T036 |
| FR-009 | Link validation | T008, T038, T039, T040 |
| FR-010 | Mermaid diagrams | T003, T035, T037 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Mermaid diagram errors will fail the build with helpful messages
- Algolia DocSearch approval is external dependency with variable timeline (days to weeks)
- Built-in search ensures search functionality works immediately without waiting for Algolia
