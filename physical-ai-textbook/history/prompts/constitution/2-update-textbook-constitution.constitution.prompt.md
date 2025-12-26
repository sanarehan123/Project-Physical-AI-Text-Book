---
id: 2
title: Update Textbook Constitution
stage: constitution
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: pc
command: /sp.constitution
labels: [constitution,physical-ai,humanoid-robotics,academic,enhancement]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: AI-Native Textbook — Physical AI & Humanoid Robotics

Purpose:
Produce an AI-native, spec-driven technical textbook for the Panaversity course "Physical AI & Humanoid Robotics", focused on embodied intelligence and AI systems operating in the physical world. The book must bridge digital AI (agents, LLMs, perception) with physical embodiment (robots, sensors, actuators) using ROS 2, Gazebo, Unity, and NVIDIA Isaac.

Educational Goal:
Enable students to design, simulate, and deploy humanoid robots capable of perception, planning, locomotion, manipulation, and natural human interaction in simulated and real-world environments.

Core principles:
- Accuracy through primary, authoritative, and verifiable sources
- Academic rigor suitable for advanced CS, AI, Robotics learners
- Reproducibility of all workflows, architectures, and experiments
- Physical realism (respect physics, embodiment, latency, constraints)
- AI-native pedagogy (agents, VLA pipelines, simulators, copilots)
- Clear separation between simulation, edge inference, and real robots

Key standards:
- Every factual, architectural, or algorithmic claim must be traceable to a source
- Citation format: APA (in-text citations + references)
- Source requirements:
  - Minimum 50% peer-reviewed sources (robotics, AI, CV, RL, HRI)
  - Remaining sources may include official documentation (ROS 2, NVIDIA Isaac, Gazebo, Unity, OpenAI, Intel RealSense)
- No hallucinated citations
- No speculative statements unless explicitly labeled as such
- Terminology must align with standard robotics and AI literature
- Plagiarism tolerance: 0% (all content must be original)
- Writing clarity target: Flesch–Kincaid grade 11–13 (technical academic audience)

Content scope & constraints:
- Book structure must align with the official course modules:
  1. Physical AI & Embodied Intelligence
  2. ROS 2 as the Robotic Nervous System
  3. Digital Twins with Gazebo & Unity
  4. NVIDIA Isaac (Perception, VSLAM, Nav2)
  5. Vision-Language-Action (VLA)
  6. Humanoid Locomotion, Manipulation, and HRI
- Weekly progression must be respected (Weeks 1–13)
- Capstone-driven design: all chapters support the final autonomous humanoid project
- Each chapter must include:
  - Learning objectives
  - Conceptual explanations
  - Architecture diagrams (text-described)
  - Practical labs or simulations
  - AI-agent interaction prompts
- Mathematical depth: conceptual-first; advanced math optional and clearly marked
- Code examples must be reproducible, minimal, and well-commented
- Hardware assumptions must match documented lab architectures (RTX workstations, Jetson Orin, sensors)

Technical & tooling constraints:
- Writing format: Markdown / MDX (Docusaurus compatible)
- Spec-first workflow using Spec-Kit Plus:
  - Chapter specs must be written before prose
  - Prose must strictly follow approved specs
- Designed for GitHub Pages deployment
- No platform-specific lock-in beyond stated tools
- Diagrams must be describable for AI rendering (no image-only explanations)

Et
```

## Response snapshot

Updated the constitution file for the AI-Native Textbook on Physical AI & Humanoid Robotics project with more specific technical requirements. Added a new principle for Physical Realism and Embodiment, updated the Course Module Alignment section with the six official course modules, and added Hardware and Platform Specifications. Enhanced existing principles with specific tooling details (ROS 2, Gazebo, Unity, NVIDIA Isaac) and VLA pipeline focus. The version was updated from 1.0.0 to 1.1.0 to reflect these material enhancements.

## Outcome

- ✅ Impact: Enhanced constitution with specific technical tooling and course structure alignment
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new principles and requirements
- 🔁 Next prompts: /sp.specify to create the feature specification based on updated constitution
- 🧠 Reflection: The updated constitution now properly reflects the specific technical requirements for the course, including ROS 2, NVIDIA Isaac, Gazebo, Unity, and VLA pipelines.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification development based on updated constitution