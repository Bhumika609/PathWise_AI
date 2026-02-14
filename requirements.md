# Requirements Document

## Introduction

PathWise AI is a voice-first eligibility reasoning and career feasibility system designed specifically for Indian students. The system extracts structured user profiles from voice or text input, evaluates eligibility for government schemes, explains decisions with clear reasoning, compares skill fit for careers, and generates actionable learning roadmaps. The system prioritizes accessibility, explainability, and responsible AI usage while serving as an MVP suitable for hackathon demonstration.

## Glossary

- **PathWise_AI**: The complete voice-first eligibility and career guidance system
- **Voice_Processor**: Component that converts speech to text and handles audio input
- **Profile_Extractor**: Component that extracts structured data from unstructured input
- **Eligibility_Engine**: Component that evaluates user eligibility for government schemes
- **Career_Matcher**: Component that compares user skills against career requirements
- **Roadmap_Generator**: Component that creates personalized learning paths
- **Government_Scheme**: Any official Indian government program for student support
- **User_Profile**: Structured representation of student's background, skills, and goals
- **Skill_Gap**: Difference between current user skills and career requirements
- **Learning_Roadmap**: Personalized sequence of learning activities and milestones

## Requirements

### Requirement 1: Voice Input Processing

**User Story:** As an Indian student, I want to provide my information through voice input, so that I can interact naturally without typing barriers.

#### Acceptance Criteria

1. WHEN a user speaks in Hindi or English, THE Voice_Processor SHALL convert speech to accurate text
2. WHEN audio quality is poor, THE Voice_Processor SHALL request clarification from the user
3. WHEN voice input is received, THE Voice_Processor SHALL handle background noise and accents common in India
4. WHEN voice processing fails, THE Voice_Processor SHALL gracefully fallback to text input mode
5. WHEN voice input contains mixed Hindi-English (Hinglish), THE Voice_Processor SHALL process it correctly

### Requirement 2: Profile Extraction

**User Story:** As a student, I want the system to understand my background from natural conversation, so that I don't need to fill complex forms.

#### Acceptance Criteria

1. WHEN unstructured text or voice input is provided, THE Profile_Extractor SHALL identify key demographic information (age, location, education level)
2. WHEN user describes their skills, THE Profile_Extractor SHALL extract and categorize technical and soft skills
3. WHEN user mentions family background, THE Profile_Extractor SHALL identify relevant socioeconomic indicators
4. WHEN incomplete information is provided, THE Profile_Extractor SHALL identify missing critical fields
5. WHEN extracted information is uncertain, THE Profile_Extractor SHALL request confirmation from the user

### Requirement 3: Government Scheme Eligibility

**User Story:** As a student, I want to know which government schemes I'm eligible for, so that I can access available support and opportunities.

#### Acceptance Criteria

1. WHEN a user profile is complete, THE Eligibility_Engine SHALL evaluate eligibility against all relevant government schemes
2. WHEN eligibility criteria are met, THE Eligibility_Engine SHALL provide clear acceptance reasoning
3. WHEN eligibility criteria are not met, THE Eligibility_Engine SHALL explain specific rejection reasons
4. WHEN eligibility is borderline, THE Eligibility_Engine SHALL suggest actions to improve eligibility
5. WHEN scheme deadlines are approaching, THE Eligibility_Engine SHALL prioritize time-sensitive opportunities

### Requirement 4: Career Skill Matching

**User Story:** As a student, I want to understand how well my skills match different career paths, so that I can make informed career decisions.

#### Acceptance Criteria

1. WHEN user skills are identified, THE Career_Matcher SHALL compare them against career requirements in the Indian job market
2. WHEN skill gaps exist, THE Career_Matcher SHALL quantify the gap size and importance
3. WHEN multiple careers are considered, THE Career_Matcher SHALL rank them by skill fit percentage
4. WHEN emerging skills are relevant, THE Career_Matcher SHALL highlight future-oriented skill requirements
5. WHEN local job market data is available, THE Career_Matcher SHALL incorporate regional career opportunities

### Requirement 5: Learning Roadmap Generation

**User Story:** As a student, I want a personalized learning plan, so that I can systematically develop skills needed for my chosen career path.

#### Acceptance Criteria

1. WHEN skill gaps are identified, THE Roadmap_Generator SHALL create a structured learning sequence
2. WHEN generating roadmaps, THE Roadmap_Generator SHALL include specific courses, certifications, and practical projects
3. WHEN timeline constraints exist, THE Roadmap_Generator SHALL prioritize high-impact learning activities
4. WHEN free resources are available, THE Roadmap_Generator SHALL prioritize accessible learning options
5. WHEN roadmaps are created, THE Roadmap_Generator SHALL include measurable milestones and progress indicators

### Requirement 6: Explainable AI Decisions

**User Story:** As a student, I want to understand why the system made specific recommendations, so that I can trust and learn from the guidance provided.

#### Acceptance Criteria

1. WHEN eligibility decisions are made, THE PathWise_AI SHALL provide step-by-step reasoning
2. WHEN career matches are suggested, THE PathWise_AI SHALL explain the matching criteria and weights used
3. WHEN roadmaps are generated, THE PathWise_AI SHALL justify the sequence and priority of learning activities
4. WHEN decisions involve uncertainty, THE PathWise_AI SHALL communicate confidence levels clearly
5. WHEN users request clarification, THE PathWise_AI SHALL provide additional detail about decision factors

### Requirement 7: Accessibility and Inclusion

**Note:** For the MVP, accessibility support is limited to voice + text interaction in English and one Indian language, with extensibility planned for future versions.

**User Story:** As a student from diverse backgrounds, I want the system to be accessible regardless of my technical literacy or physical abilities, so that I can benefit from career guidance.

#### Acceptance Criteria

1. WHEN users have limited technical skills, THE PathWise_AI SHALL provide simple, intuitive interactions
2. WHEN users have hearing impairments, THE PathWise_AI SHALL support text-based alternatives to voice
3. WHEN users speak regional languages, THE PathWise_AI SHALL handle common Indian language patterns
4. WHEN users have slow internet connections, THE PathWise_AI SHALL function with minimal bandwidth requirements
5. WHEN users access from mobile devices, THE PathWise_AI SHALL provide responsive, mobile-optimized interfaces

### Requirement 8: Data Privacy and Security

**Note**: For the hackathon MVP, data privacy measures are demonstrated conceptually and through design choices rather than full production-grade implementation.

**User Story:** As a student sharing personal information, I want my data to be protected and used responsibly, so that my privacy is maintained.

#### Acceptance Criteria

1. WHEN personal data is collected, THE PathWise_AI SHALL obtain explicit user consent
2. WHEN data is stored, THE PathWise_AI SHALL encrypt sensitive information
3. WHEN data is processed, THE PathWise_AI SHALL minimize data collection to essential information only
4. WHEN users request data deletion, THE PathWise_AI SHALL remove all personal information completely
5. WHEN data is shared with external services, THE PathWise_AI SHALL anonymize user information

### Requirement 9: Government Scheme Database

**Note**: For the MVP, the system will demonstrate functionality using a small curated set of 3–5 representative government schemes.

**User Story:** As a system administrator, I want to maintain current information about government schemes, so that students receive accurate and up-to-date guidance.

#### Acceptance Criteria

1. THE PathWise_AI SHALL maintain a comprehensive database of Indian government schemes for students
2. WHEN scheme information changes, THE PathWise_AI SHALL update eligibility criteria and application processes
3. WHEN new schemes are announced, THE PathWise_AI SHALL incorporate them into the evaluation system
4. WHEN schemes expire or are discontinued, THE PathWise_AI SHALL remove them from active consideration
5. WHEN scheme data is uncertain, THE PathWise_AI SHALL flag information that requires verification

### Requirement 10: MVP Demonstration Capabilities

**User Story:** As a hackathon participant, I want to demonstrate core system capabilities effectively, so that judges can understand the system's value proposition.

#### Acceptance Criteria

1. WHEN demonstrating the system, THE PathWise_AI SHALL complete end-to-end workflows within 3 minutes
2. WHEN processing sample inputs, THE PathWise_AI SHALL show clear before/after comparisons
3. WHEN explaining decisions, THE PathWise_AI SHALL provide visual representations of reasoning
4. WHEN showcasing features, THE PathWise_AI SHALL handle realistic Indian student scenarios
5. WHEN technical issues occur, THE PathWise_AI SHALL have fallback demonstration modes