import type { Config } from '@docusaurus/types';
import { themes as prismThemes } from 'prism-react-renderer';

const config: Config = {
  title: 'Hackathon III',
  tagline: 'Reusable Intelligence and Cloud-Native Mastery',
  favicon: 'img/favicon.ico',

  url: 'https://github.com/MathNj/Learn-Flow',
  baseUrl: '/',

  organizationName: 'Hackathon III',
  projectName: 'Hackathon3',

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
          editUrl: 'https://github.com/MathNj/Learn-Flow/tree/main/docs-site',
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
      title: 'Hackathon III',
      logo: {
        alt: 'Hackathon III Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/MathNj/Learn-Flow',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            { label: 'Getting Started', to: '/docs/getting-started/installation' },
            { label: 'Skills Library', to: '/docs/skills-library/playbook' },
            { label: 'Architecture', to: '/docs/architecture/overview' },
          ],
        },
        {
          title: 'Project',
          items: [
            { label: 'GitHub', href: 'https://github.com/MathNj/Learn-Flow' },
            { label: 'Score: 87/100', to: '/docs/' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Hackathon III. Built with Docusaurus.`,
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
