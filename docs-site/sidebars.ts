import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'index',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Getting Started',
      link: {
        type: 'generated-index',
        title: 'Getting Started',
        description: 'Get up and running with {{SITE_NAME}}',
        slug: '/getting-started',
      },
      items: [
        { type: 'doc', id: 'getting-started/installation', label: 'Installation' },
        { type: 'doc', id: 'getting-started/quick-start', label: 'Quick Start' },
        { type: 'doc', id: 'getting-started/environment', label: 'Environment Setup' },
      ],
    },
    {
      type: 'category',
      label: 'Skills Library',
      link: {
        type: 'generated-index',
        title: 'Skills Library',
        description: 'Overview of available skills and development guides',
        slug: '/skills-library',
      },
      items: [
        { type: 'doc', id: 'skills-library/overview', label: 'Overview' },
        { type: 'doc', id: 'skills-library/development', label: 'Development Guide' },
        { type: 'doc', id: 'skills-library/mcp-pattern', label: 'MCP Code Execution Pattern' },
        { type: 'doc', id: 'skills-library/token-efficiency', label: 'Token Efficiency' },
      ],
    },
    {
      type: 'category',
      label: 'Architecture',
      link: {
        type: 'generated-index',
        title: 'Architecture',
        description: 'System architecture and design decisions',
        slug: '/architecture',
      },
      items: [
        { type: 'doc', id: 'architecture/overview', label: 'System Overview' },
        { type: 'doc', id: 'architecture/microservices', label: 'Microservices' },
        { type: 'doc', id: 'architecture/event-flow', label: 'Event Flow' },
        { type: 'doc', id: 'architecture/technology', label: 'Technology Choices' },
      ],
    },
    {
      type: 'category',
      label: 'API Documentation',
      link: {
        type: 'generated-index',
        title: 'API Documentation',
        description: 'REST APIs, Kafka topics, and WebSocket events',
        slug: '/api',
      },
      items: [
        { type: 'doc', id: 'api/rest', label: 'REST API' },
        { type: 'doc', id: 'api/kafka', label: 'Kafka Topics' },
        { type: 'doc', id: 'api/websocket', label: 'WebSocket' },
        { type: 'doc', id: 'api/authentication', label: 'Authentication' },
      ],
    },
    {
      type: 'category',
      label: 'Deployment',
      link: {
        type: 'generated-index',
        title: 'Deployment',
        description: 'Deployment guides and troubleshooting',
        slug: '/deployment',
      },
      items: [
        { type: 'doc', id: 'deployment/kubernetes', label: 'Kubernetes' },
        { type: 'doc', id: 'deployment/cloud', label: 'Cloud Deployment' },
        { type: 'doc', id: 'deployment/cicd', label: 'CI/CD' },
        { type: 'doc', id: 'deployment/troubleshooting', label: 'Troubleshooting' },
      ],
    },
    {
      type: 'category',
      label: 'LearnFlow Platform',
      link: {
        type: 'generated-index',
        title: 'LearnFlow Platform',
        description: 'User guides for the LearnFlow learning platform',
        slug: '/learnflow',
      },
      items: [
        { type: 'doc', id: 'learnflow/user-guide', label: 'User Guide' },
        { type: 'doc', id: 'learnflow/teacher-guide', label: 'Teacher Guide' },
        { type: 'doc', id: 'learnflow/student-guide', label: 'Student Guide' },
      ],
    },
  ],
};

export default sidebars;
