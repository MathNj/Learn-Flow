# Search Configuration Reference

This reference covers search setup for Docusaurus documentation sites.

## Algolia DocSearch

### Setup

1. Apply for DocSearch at https://docsearch.algolia.com/
2. Wait for approval (usually 1-3 days)
3. Configure your site

### Configuration

```typescript
// docusaurus.config.ts
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'YOUR_INDEX_NAME',
    contextualSearch: true,
    searchParameters: {
      facetFilters: ['version:VERSION'],
    },
  },
};
```

### DocSearch Styles

Algolia DocSearch provides its own UI. No additional CSS needed.

### Search Parameters

```typescript
searchParameters: {
  hitsPerPage: 5,
  maxValuesPerFacet: 10,
  facetFilters: ['lang:en', 'version:1.0'],
}
```

## Local Search (Alternative)

### Installation

```bash
npm install @easyops-cn/docusaurus-theme-local-search
```

### Configuration

```typescript
// docusaurus.config.ts
themes: [
  [
    require.resolve('@easyops-cn/docusaurus-theme-local-search'),
    {
      hashed: true,
      indexDocs: true,
      indexBlog: false,
      indexPages: true,
      language: ['en'],
      highlightSearchTermsOnTargetPage: true,
      explicitSearchResultPath: true,
    },
  ],
];
```

### Search Component

Add to navbar:

```typescript
themeConfig: {
  navbar: {
    items: [
      {
        type: 'search',
        position: 'right',
      },
    ],
  },
};
```

## Search Result Ranking

### Algolia Ranking

Algolia uses:
- Text relevance
- Geographic location (if enabled)
- Custom ranking rules

Configure in Algolia dashboard:
1. Go to Ranking
2. Set custom ranking (attribute, desc(createdAt), etc.)
3. Configure facets

### Local Search Ranking

Local search uses FlexSearch:
- Term frequency
- Document frequency
- Field weights

```typescript
// Configure weights
searchResultLimits: 8,
searchResultContextMaxLength: 50,
```

## Indexing Control

### Exclude from Search

```markdown
---
search: false
---

This page won't be indexed.
```

### Custom Search Snippets

```markdown
---
description: This is the search snippet
---

Page content...
```

## Performance

### Index Size

- Algolia: Managed by Algolia
- Local search: ~100KB per 100 pages

### Search Speed

- Algolia: <100ms (SC-003 target)
- Local search: <50ms (typically faster)

### Optimization

```typescript
// Debounce search input
// Lazy load search index
// Use web workers for local search
```

## Troubleshooting

### Algolia Issues

**Problem:** Search returns no results

**Solutions:**
- Verify API key has search permissions
- Check index name matches
- Wait for crawl to complete (24-48 hours)

**Problem:** Outdated results

**Solutions:**
- Trigger re-crawl in Algolia dashboard
- Check sitemap.xml is accessible

### Local Search Issues

**Problem:** Search not working

**Solutions:**
- Verify theme is installed
- Check `hashed: true` for production
- Ensure `indexDocs: true`

**Problem:** Large bundle size

**Solutions:**
- Use `hashed: true`
- Index only docs, not all pages
- Limit `searchResultLimits`
