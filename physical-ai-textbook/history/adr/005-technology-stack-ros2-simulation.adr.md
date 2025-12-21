# ADR-005: Technology Stack - ROS 2, Gazebo, Unity, and NVIDIA Isaac Sim

## Title
Technology Stack - ROS 2, Gazebo, Unity, and NVIDIA Isaac Sim

## Context
The Physical AI & Humanoid Robotics textbook needs to select core technologies for the curriculum that represent industry standards while being accessible to students. The technology stack must support the simulation-first pedagogy and align with the course's focus on humanoid robotics and Vision-Language-Action systems. Multiple robotics frameworks and simulation environments exist with different strengths and weaknesses.

## Decision
We will use ROS 2 as the primary robotics middleware, Gazebo for physics simulation and sensor modeling, Unity for human-robot interaction visualization, and NVIDIA Isaac Sim for photorealistic simulation and synthetic data generation. This combination provides comprehensive coverage of the robotics development pipeline.

## Alternatives Considered
1. ROS 1 vs ROS 2 - ROS 2 chosen for modern features and long-term support
2. Gazebo vs PyBullet vs Mujoco vs Webots - Gazebo chosen for ROS integration and physics accuracy
3. Unity vs Unreal Engine vs Godot - Unity chosen for robotics community adoption
4. NVIDIA Isaac Sim vs CoppeliaSim vs AirSim - Isaac Sim chosen for AI/ML integration
5. Alternative frameworks like MoveIt vs custom solutions

## Tradeoffs
**Benefits:**
- Industry-standard technologies used in professional robotics
- Strong community support and documentation
- Comprehensive simulation capabilities
- Integration with AI/ML workflows
- Extensive learning resources available
- Compatible with hardware platforms

**Costs/Risks:**
- Complex setup and configuration requirements
- Hardware requirements (especially for Isaac Sim)
- Learning curve for multiple tools
- Potential compatibility issues between tools
- Maintenance of multiple technology dependencies
- Licensing considerations for commercial tools

## Consequences
- Students learn industry-standard tools and workflows
- Curriculum requires RTX workstation or equivalent hardware
- Content must address setup and configuration challenges
- Multiple tutorials needed for different toolchains
- Hardware requirements may limit accessibility
- Future technology updates require coordinated curriculum updates