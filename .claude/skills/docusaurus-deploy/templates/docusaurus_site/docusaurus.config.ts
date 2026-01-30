import type { Config } from '@docusaurus/types';
import { themes as prismThemes } from 'prism-react-renderer';

const config: Config = {
  title: '{{SITE_NAME}}',
  tagline: '{{SITE_TAGLINE}}',
  favicon: 'img/favicon.ico',

  url: '{{SITE_URL}}',
  baseUrl: '{{BASE_URL}}',

  organizationName: '{{ORG_NAME}}',
  projectName: '{{PROJECT_NAME}}',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  onBrokenAnchors: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: '{{EDIT_URL}}',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: ['./src/css/custom.css'],
        },
      } as const),
    ],
  ],

  themes: [
    [
      require.resolve('@docusaurus/theme-mermaid'),
      {
        theme: { theme: 'default' },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: '{{SITE_NAME}}',
      logo: {
        alt: '{{SITE_NAME}} Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: '{{GITHUB_URL}}',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Getting Started', to: '/docs/getting-started/installation' },
            { label: 'Architecture', to: '/docs/architecture/overview' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'GitHub', href: '{{GITHUB_URL}}' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'Blog', to: '/blog' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} {{ORG_NAME}}. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'typescript', 'yaml', 'bash', 'json'],
    },
    mermaid: {
      theme: { light: 'default', dark: 'dark' },
    },
  } satisfies Preset.ThemeConfig,

  markdown: {
    mermaid: true,
  },
};

export default config;
