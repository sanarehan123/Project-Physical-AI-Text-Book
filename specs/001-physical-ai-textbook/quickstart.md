# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Development

## Prerequisites
- Node.js LTS version (18.x or higher)
- npm package manager
- Git
- Python 3.8+ for ROS 2 development
- Basic knowledge of ROS 2, Python, and robotics concepts
- Access to RTX workstation or equivalent for simulation

## Setup Instructions

### 1. Environment Setup
```bash
# Clone the textbook repository
git clone [repository-url]
cd physical-ai-humanoid-robotics

# Install Docusaurus dependencies
npm install
```

### 2. Local Development
```bash
# Start the development server
npm start

# This opens the textbook in your browser with hot reloading
# Most changes are reflected live without restarting the server
```

### 3. Building the Textbook
```bash
# Generate static content for production
npm run build

# This creates a build directory with the static site
```

### 4. Adding New Content
1. Create new MDX files in the appropriate module directory (`docs/module-X/`)
2. Follow the standardized chapter template with:
   - Learning objectives
   - Conceptual foundations
   - System architecture explanation
   - Practical labs/simulations
   - AI-agent interaction prompts
   - Summary and readiness checks
3. Add the new file to the sidebar configuration in `sidebars.ts`
4. Ensure all citations follow APA format
5. Test locally before committing

## Architecture Overview

### Content Structure
The textbook follows a 4-module, 16-chapter structure:
- **Module 1**: Foundations of Physical AI & Embodied Intelligence (Chapters 1-4)
- **Module 2**: The Robotic Nervous System (ROS 2) (Chapters 5-8)
- **Module 3**: Digital Twins & AI-Robot Brains (Chapters 9-12)
- **Module 4**: Vision-Language-Action & Capstone (Chapters 13-16)

### Technology Stack
- **Framework**: Docusaurus v3+ with MDX support
- **Language**: TypeScript for configuration
- **Content**: Markdown/MDX with embedded React components
- **Deployment**: GitHub Pages via GitHub Actions
- **Simulation Tools**: Gazebo, Unity, NVIDIA Isaac Sim
- **Middleware**: ROS 2 with Python agents

## Development Workflow

### Writing Process
1. Research phase: Identify sources and claims for each chapter
2. Foundation phase: Write core explanations and architecture descriptions
3. Analysis phase: Compare methods, tools, and approaches
4. Synthesis phase: Integrate concepts toward capstone readiness

### Quality Assurance
- Every technical claim must have a verifiable source
- Minimum 50% peer-reviewed sources requirement
- APA citation format enforcement
- AI-agent prompts required in every chapter
- Text-described diagrams for AI rendering

### Validation Checks
- Content-level: Citations, formatting, completeness
- Structural: Build process, navigation, links
- Pedagogical: Learning objectives, capstone progression
- AI-native: Agent prompts functionality

## Key Configuration Files
- `docusaurus.config.ts`: Main site configuration
- `sidebars.ts`: Navigation structure
- `package.json`: Dependencies and scripts
- `tsconfig.json`: TypeScript configuration

## Simulation Environment Setup
For chapters involving practical labs:
1. Install ROS 2 (Humble Hawksbill or later)
2. Set up Gazebo Garden for physics simulation
3. Configure NVIDIA Isaac Sim for photorealistic environments
4. Install Unity for human-robot interaction visualization

## Academic Standards
- Factual claims must be traceable to authoritative sources
- No hallucinated citations allowed
- Terminology aligned with standard robotics and AI literature
- Mathematical depth: conceptual-first, advanced derivations marked as optional
- Plagiarism tolerance: 0% (all content must be original)

## Deployment
The textbook is automatically deployed via GitHub Actions to GitHub Pages when changes are pushed to the main branch. The base URL will be configured as `/physical-ai-humanoid-robotics/` for GitHub Pages hosting.