# ADR-002: Simulation-First Pedagogy with Real Hardware Extensions

## Title
Simulation-First Pedagogy with Real Hardware Extensions

## Context
The Physical AI & Humanoid Robotics textbook needs to balance accessibility and safety with real-world experience. Students need to learn robotics concepts without requiring expensive hardware or risking damage to equipment. The curriculum must prepare students for real hardware work while remaining accessible to institutions with limited resources.

## Decision
We will adopt a simulation-first approach using Gazebo, Unity, and NVIDIA Isaac Sim for the majority of learning experiences, with optional real hardware extensions noted throughout the content. This provides a safe, cost-effective learning environment while maintaining the ability to transfer skills to real robots.

## Alternatives Considered
1. Hardware-first approach - Direct interaction with physical robots from the start
2. Simulation-only approach - No real hardware integration at all
3. Parallel tracks - Separate simulation and hardware curricula
4. Hardware loan programs - Institutions borrow robots for courses
5. Cloud robotics platforms - Remote access to physical robots

## Tradeoffs
**Benefits:**
- Cost-effective for educational institutions
- Safe learning environment without risk of damaging expensive equipment
- Consistent experience across different institutions
- Ability to simulate dangerous or complex scenarios safely
- Faster iteration and experimentation
- Scalable to large classes

**Costs/Risks:**
- Sim-to-real transfer gap may limit learning
- Less hands-on experience with physical constraints
- Students may not fully appreciate real-world challenges
- Additional cognitive load when transitioning to real hardware
- Simulation accuracy limitations

## Consequences
- Students develop theoretical and simulation-based skills first
- Curriculum must explicitly address sim-to-real challenges
- Hardware extension activities need to be clearly marked
- Institutions can adopt curriculum without major hardware investments
- Content must acknowledge and explain simulation limitations
- Future hardware updates require minimal curriculum changes