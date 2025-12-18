// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Manual sidebar for the Physical AI & Humanoid Robotics textbook
  textbookSidebar: [
    {
      type: 'category',
      label: 'Module 1 - Foundations of Physical AI & Embodied Intelligence',
      link: {type: 'doc', id: 'module-1/index'},
      items: [
        'module-1/chapter-1-introduction-to-physical-ai',
        'module-1/chapter-2-humanoid-robotics-landscape',
        'module-1/chapter-3-sensors-as-perception-organs',
        'module-1/chapter-4-physical-constraints-reality-gaps'
      ]
    },
    {
      type: 'category',
      label: 'Module 2 - The Robotic Nervous System (ROS 2)',
      link: {type: 'doc', id: 'module-2/index'},
      items: [
        'module-2/chapter-5-ros-2-architecture',
        'module-2/chapter-6-python-agents-with-ros-2',
        'module-2/chapter-7-robot-description-urdf',
        'module-2/chapter-8-ros-2-systems-engineering'
      ]
    },
    {
      type: 'category',
      label: 'Module 3 - Digital Twins & AI-Robot Brains',
      link: {type: 'doc', id: 'module-3/index'},
      items: [
        'module-3/chapter-9-gazebo-physics-simulation',
        'module-3/chapter-10-unity-human-robot-interaction',
        'module-3/chapter-11-nvidia-isaac-sim',
        'module-3/chapter-12-isaac-ros-navigation'
      ]
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action & Capstone',
      link: {type: 'doc', id: 'module-4/index'},
      items: [
        'module-4/chapter-13-vision-humanoid-robots',
        'module-4/chapter-14-language-control-interface',
        'module-4/chapter-15-vision-language-action',
        'module-4/chapter-16-autonomous-humanoid-capstone'
      ]
    }
  ]
};

export default sidebars;
