---
id: 1
title: Create Textbook Constitution
stage: constitution
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: pc
command: /sp.constitution
labels: [constitution,physical-ai,humanoid-robotics,academic]
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

Project: AI-Native Textbook on Physical AI & Humanoid Robotics

Purpose:
Create an AI-native, spec-driven technical textbook for Panaversity that teaches Physical AI and Humanoid Robotics using reproducible, verifiable, and academically rigorous content, deployable via Docusaurus and GitHub Pages.

Core principles:
- Accuracy through primary and authoritative source verification
- Clarity for a technical audience (computer science, AI, robotics background)
- Reproducibility (all claims, algorithms, and workflows must be traceable)
- Rigor (peer-reviewed and industry-standard sources preferred)
- AI-native pedagogy (agents, simulations, and embodied intelligence emphasized)

Key standards:
- All factual and technical claims must be traceable to credible sources
- Citation format: APA style
- Source types:
  - Minimum 50% peer-reviewed academic papers (journals, conferences)
  - Remaining sources may include robotics documentation, standards, and reputable industry research (e.g., ROS, OpenAI, DeepMind, NVIDIA, Boston Dynamics)
- No speculative claims without explicit labeling
- Terminology must be consistent with robotics and AI literature
- Plagiarism tolerance: 0% (all text must be original)
- Writing clarity target: Flesch-Kincaid grade level 11–13 (advanced technical audience)

Content constraints:
- Total length: 12–16 chapters (equivalent to a full semester textbook)
- Each chapter must include:
  - Clear learning objectives
  - Conceptual explanation
  - Practical examples or simulations
  - AI-agent interaction prompts
- Minimum 30–40 total sources across the book
- Mathematical depth: conceptual explanations preferred; advanced math optional and clearly marked
- Code examples must be reproducible and clearly annotated

Technical constraints:
- Writing format: Markdown / MDX (Docusaurus compatible)
- Structure driven by Spec-Kit Plus specifications
- Chapters generated from spec files before prose expansion
- No hard-coded assumptions about hardware; abstractions preferred
- All dia
```

## Response snapshot

Created the constitution file for the AI-Native Textbook on Physical AI & Humanoid Robotics project. The constitution includes six core principles covering academic rigor, technical clarity, reproducibility, AI-native pedagogy, zero plagiarism standards, and comprehensive structure. It also includes technical standards, development workflow, and governance sections. The file is located at .specify/memory/constitution.md and follows all specified requirements.

## Outcome

- ✅ Impact: Created initial project constitution with all required principles and standards
- 🧪 Tests: none
- 📁 Files: Created .specify/memory/constitution.md with 100% coverage of specified requirements
- 🔁 Next prompts: /sp.specify to create the feature specification
- 🧠 Reflection: The constitution successfully captures all the core principles and constraints specified by the user, providing a solid foundation for the textbook development.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification development based on this constitution