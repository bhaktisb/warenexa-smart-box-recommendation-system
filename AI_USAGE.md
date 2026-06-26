# AI Usage Statement

# AI Usage Documentation

## Project

**Smart Box Recommendation System**

Developed for the fictional company **WareNexa Technologies Pvt. Ltd.**

---

# Purpose

Artificial Intelligence (AI) tools were used during the software development process to improve productivity, accelerate research, review architectural decisions, and assist with implementation. All final technical decisions, system design, business rules, testing, and validation were reviewed and approved by the project author.

---

# AI Tools Used

| Tool           | Purpose                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| ChatGPT        | Business analysis, SDLC planning, BRD, SRS, architecture design, algorithm discussions, documentation, code reviews, interview preparation |
| Cursor AI      | Django implementation, code generation, refactoring, debugging, GitHub Actions, documentation updates                                      |
| GitHub Copilot | Code completion and productivity during development                                                                                        |
| Claude         | Architecture reviews, engineering audits, recommendation algorithm evaluation, documentation feedback                                      |

---

# AI-Assisted Development Process

AI tools were used as engineering assistants rather than autonomous developers.

The development followed a structured Software Development Life Cycle (SDLC):

1. Business Domain Analysis
2. Business Requirements Document (BRD)
3. Software Requirements Specification (SRS)
4. System Architecture
5. Database Design
6. Recommendation Algorithm Design
7. Django Implementation
8. Testing
9. Documentation
10. Deployment Preparation

The project architecture was finalized before implementation to ensure consistency throughout development.

---

# Example Prompt Categories

Examples of prompts provided to AI tools included:

* Analyze the warehouse business domain.
* Review the system architecture.
* Compare packing algorithms.
* Generate Django project structure.
* Review code quality.
* Improve Django best practices.
* Create GitHub Actions CI workflow.
* Review security and production readiness.
* Generate technical documentation.
* Prepare interview questions.

---

# Accepted AI Suggestions

The following AI suggestions were accepted after technical review:

* Layered architecture using Django service classes.
* PAME (Per-Axis Maximum Envelope) packing algorithm.
* Warehouse-oriented workflow.
* GitHub Actions CI pipeline.
* Improved validation rules.
* Logging configuration.
* Authentication for warehouse operations.
* Query optimization using Django ORM.
* Production readiness improvements.

---

# Rejected AI Suggestions

Some AI-generated recommendations were intentionally rejected because they exceeded the project scope or conflicted with the approved architecture.

Examples include:

* Full 3D bin-packing implementation.
* Microservices architecture.
* Docker and Kubernetes deployment.
* Redis and Celery integration.
* PostgreSQL-only configuration.
* Domain event architecture.
* Excessive production infrastructure.
* Automatic redesign of the database schema after implementation.

These suggestions were considered valuable for enterprise systems but unnecessary for the educational scope of this project.

---

# Challenges and Corrections

During development, several issues were identified and resolved through engineering review:

* Initial packing algorithm produced overly conservative box recommendations.
* Business rules were refined to better reflect warehouse operations.
* Recommendation engine was updated to use the approved PAME algorithm.
* Documentation and implementation were synchronized after architectural changes.
* Test cases were expanded to verify business scenarios and edge cases.

---

# Verification Process

Every AI-generated output was manually reviewed before being accepted.

Verification included:

* Requirement validation against BRD and SRS.
* Architecture consistency checks.
* Manual code review.
* Django system checks.
* Unit testing.
* Integration testing.
* Functional testing using demo orders.
* User interface verification.
* GitHub Actions CI validation.

No AI-generated code was accepted without review and testing.

---

# Human Contributions

The project author was responsible for:

* Selecting the business domain.
* Defining project scope.
* Designing the software architecture.
* Approving business rules.
* Choosing the recommendation algorithm.
* Reviewing AI-generated code.
* Testing functionality.
* Making final engineering decisions.
* Preparing documentation and project artifacts.

AI tools were used to assist with implementation and review, but final responsibility for the project remained with the author.

---

# Disclaimer

This project demonstrates responsible AI-assisted software development. AI tools were used to improve productivity while maintaining human oversight over architecture, implementation, testing, and decision-making. All final deliverables were validated before inclusion in the project.
