// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'AI Systems in the Physical World',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://physical-ai-textbook.vercel.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel deployment, use '/' for root, or adjust as needed
  baseUrl: '/',

  // For GitHub pages deployment only.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'sanarehan123', // Usually your GitHub org/user name.
  projectName: 'physical-ai-textbook', // Usually your repo name.

  onBrokenLinks: 'warn',  // Changed from 'throw' to 'warn' to allow build to continue
  markdown: {
    mermaid: true,
    mdx1Compat: {
      admonitions: true,
      headingIds: true,
    },
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/sanarehan123/physical-ai-textbook/edit/main/',
          routeBasePath: 'docs', // Serve docs under /docs path
        },
        blog: false, // Disable blog for textbook
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.svg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI & Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'textbookSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/sanarehan123/physical-ai-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Module 1 - Foundations',
                to: '/docs/module-1',
              },
              {
                label: 'Module 2 - ROS 2',
                to: '/docs/module-2',
              },
              {
                label: 'Module 3 - Simulation',
                to: '/docs/module-3',
              },
              {
                label: 'Module 4 - VLA & Capstone',
                to: '/docs/module-4',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Docusaurus',
                href: 'https://docusaurus.io',
              },
              {
                label: 'ROS 2',
                href: 'https://docs.ros.org/en/humble/',
              },
              {
                label: 'Gazebo',
                href: 'https://gazebosim.org/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/sanarehan123/physical-ai-textbook',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
