# ADR-001: Textbook Platform Architecture - Docusaurus with MDX and GitHub Pages

## Title
Textbook Platform Architecture - Docusaurus with MDX and GitHub Pages

## Context
The Physical AI & Humanoid Robotics textbook needs a platform for deployment that supports rich content with embedded AI-agent prompts, simulation content, and academic citations. The platform must be accessible to students, support version control, and allow for easy maintenance and updates. Multiple options were available including custom web frameworks, static site generators, and learning management systems.

## Decision
We will use Docusaurus as the documentation framework with MDX format for content, deployed via GitHub Pages. This provides a proven documentation platform with support for React components, versioning, search, and responsive design.

## Alternatives Considered
1. Custom React application with Next.js - More flexibility but higher maintenance overhead
2. GitBook - Good documentation features but less customization capability
3. Traditional LMS platform (Moodle, Canvas) - More educational features but less flexible for AI-native content
4. Static site generator with Eleventy - Simpler but less documentation-focused features
5. Hugo with Docsy theme - Alternative documentation framework but steeper learning curve

## Tradeoffs
**Benefits:**
- Rich content support with MDX (Markdown + React components)
- Built-in search, navigation, and responsive design
- GitHub integration for version control and collaboration
- Community support and active development
- Free hosting via GitHub Pages
- Support for multiple versions and languages

**Costs/Risks:**
- Learning curve for Docusaurus-specific features
- Potential build time constraints with GitHub Pages
- Less control over hosting compared to self-hosted solutions
- Dependency on Docusaurus ecosystem updates

## Consequences
- Content authors must learn MDX syntax and Docusaurus conventions
- Build process must remain under GitHub Pages limits (5 minutes)
- Content structure follows Docusaurus sidebar conventions
- Deployment is automated via GitHub Actions
- AI-agent prompts can be embedded as React components
- Citations and academic formatting require custom components
- Future contributors need to understand Docusaurus configuration