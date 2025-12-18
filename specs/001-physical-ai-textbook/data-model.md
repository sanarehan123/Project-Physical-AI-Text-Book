# Data Model: Physical AI & Humanoid Robotics Textbook

## Chapter Entity
- **id**: Unique identifier for the chapter (e.g., "chapter-1-introduction-to-physical-ai")
- **title**: Display title of the chapter
- **moduleId**: Reference to the parent module
- **learningObjectives**: Array of measurable learning outcomes
- **conceptualFoundations**: High-level explanations grounded in physical reality
- **systemArchitecture**: Text-described diagrams and architecture explanations
- **practicalLabs**: Array of simulation-based exercises and activities
- **aiAgentPrompts**: Array of tutor, debugging, and explanation prompts
- **summary**: Key takeaways and capstone relevance
- **citations**: Array of APA-formatted references
- **position**: Chapter number within the module (1-4) and overall sequence (1-16)

## Module Entity
- **id**: Unique identifier for the module (e.g., "module-1-foundations")
- **title**: Module title and theme
- **description**: Overview of module content and objectives
- **chapters**: Array of chapter references in sequence
- **learningPath**: Prerequisites and connections to other modules
- **capstoneAlignment**: How the module supports the final capstone project
- **position**: Module number (1-4)

## LearningObjective Entity
- **id**: Unique identifier for the objective
- **text**: Clear, measurable outcome statement
- **moduleId**: Reference to the parent module
- **chapterId**: Reference to the parent chapter
- **type**: Category (conceptual, practical, analytical, capstone-relevant)

## PracticalLab Entity
- **id**: Unique identifier for the lab
- **title**: Lab title and purpose
- **moduleId**: Reference to the parent module
- **chapterId**: Reference to the parent chapter
- **requirements**: Software/hardware requirements (simulation-first)
- **steps**: Sequential steps for completing the lab
- **expectedOutcome**: What students should achieve
- **tools**: Tools used (Gazebo, Isaac Sim, ROS 2, etc.)
- **complexity**: Difficulty level (beginner, intermediate, advanced)

## AIAgentPrompt Entity
- **id**: Unique identifier for the prompt
- **type**: Category (tutor, debugging, explanation)
- **context**: When this prompt should be used
- **promptText**: The actual prompt for the AI agent
- **moduleId**: Reference to the parent module
- **chapterId**: Reference to the parent chapter
- **targetAudience**: Specific audience the prompt addresses

## Citation Entity
- **id**: Unique identifier for the citation
- **type**: Source type (peer-reviewed, documentation, industry)
- **apaFormat**: Full APA-formatted citation
- **url**: Optional URL for online sources
- **verificationStatus**: Status of source verification
- **usedIn**: Array of chapters where this citation is used
- **recency**: Publication year for recency tracking

## Textbook Entity
- **title**: "Physical AI & Humanoid Robotics"
- **subtitle**: "AI Systems in the Physical World"
- **modules**: Array of module references in sequence
- **totalChapters**: 16 (4 modules × 4 chapters each)
- **targetAudience**: Advanced undergraduate and graduate students, AI engineers, educators
- **learningOutcomes**: Overall outcomes students should achieve
- **prerequisites**: Assumed knowledge and skills
- **capstoneProject**: Description of the final autonomous humanoid project

## ContentValidation Entity
- **id**: Unique identifier for the validation check
- **type**: Type of validation (citation, technical accuracy, terminology, plagiarism)
- **requirement**: Specific requirement being validated
- **testMethod**: How the validation is performed
- **frequency**: How often validation occurs (per chapter, per module, continuous)
- **responsibleParty**: Who performs the validation (author, peer reviewer, automated tool)

## ArchitectureDiagram Entity
- **id**: Unique identifier for the diagram
- **title**: Diagram title
- **moduleId**: Reference to the parent module
- **chapterId**: Reference to the parent chapter
- **description**: Text-based description of the diagram (AI-renderable)
- **dataFlow**: Description of data flows in the diagram
- **components**: List of system components shown
- **relationships**: Description of relationships between components