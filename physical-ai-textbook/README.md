# Physical AI & Humanoid Robotics Textbook

This repository contains the source code for the "Physical AI & Humanoid Robotics" AI-native textbook, built with Docusaurus.

## About

This textbook teaches embodied intelligence by guiding learners from digital AI systems to humanoid robots acting in simulated and physical environments using ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action (VLA) pipelines.

## Structure

The textbook is organized into 4 modules with 4 chapters each (16 chapters total):

- **Module 1**: Foundations of Physical AI & Embodied Intelligence
- **Module 2**: The Robotic Nervous System (ROS 2)
- **Module 3**: Digital Twins & AI-Robot Brains
- **Module 4**: Vision-Language-Action & Capstone

## Development

### Installation

```bash
npm install
```

### Local Development

```bash
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

This site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

## Contributing

This textbook was developed using Spec-Kit Plus and Claude Code with a spec-driven development approach. All content follows the architectural decisions documented in the `history/adr/` directory.

## License

This textbook is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
