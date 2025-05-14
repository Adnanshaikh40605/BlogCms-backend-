# Contributing to Blog CMS

Thank you for considering contributing to the Blog CMS project! This document outlines the process for contributing to the project and provides guidelines to help you get started.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Issue Reporting](#issue-reporting)

## Code of Conduct ---

We expect all contributors to adhere to our code of conduct, which can be summarized as:

- Be respectful and inclusive
- Be collaborative
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork
3. Set up your development environment using the instructions in the README.md
4. Create a new branch for your feature or bugfix

## Development Workflow

We follow a Git Flow-inspired workflow:

- `main` branch contains production-ready code
- `develop` branch is where features are integrated
- Feature branches should be created from `develop`
- Use `feature/feature-name` for new features
- Use `bugfix/issue-description` for bug fixes

### Example workflow:

```bash
# Clone your fork
git clone https://github.com/your-username/blog-cms.git

# Set up upstream remote
git remote add upstream https://github.com/original-org/blog-cms.git

# Create a feature branch from develop
git checkout develop
git pull upstream develop
git checkout -b feature/my-awesome-feature

# Make your changes...

# Push to your fork
git push origin feature/my-awesome-feature
```

## Coding Standards

### Backend (Python/Django)

- Follow PEP 8 style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Write docstrings for all functions and classes
- Use type hints when possible
- Organize imports alphabetically
- Maximum line length: 88 characters

### Frontend (JavaScript/React)

- Follow the Airbnb JavaScript Style Guide
- Use ESLint for code linting
- Use Prettier for code formatting
- Use functional components with hooks (preferred over class components)
- Use PropTypes or TypeScript for type checking
- Organize imports: React, third-party packages, local components, styles

## Testing Guidelines

### Backend Testing

- Write unit tests for all models, views, and services
- Use pytest for running tests
- Aim for at least 80% code coverage

```bash
# Run backend tests
cd backend
pytest

# Run with coverage
pytest --cov=.
```

### Frontend Testing

- Write unit tests for components and hooks
- Use Jest and React Testing Library
- Test component rendering and interactions
- Mock API calls when necessary

```bash
# Run frontend tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage
```

## Pull Request Process

1. Ensure your code adheres to the coding standards
2. Run all tests and ensure they pass
3. Update documentation if necessary
4. Rebase your branch on the latest develop branch
5. Create a pull request to merge into the develop branch
6. Include a clear description of the changes
7. Reference any related issues
8. Wait for code review and address any feedback

### Pull Request Template

When creating a pull request, please include:

- **Description**: What changes does this PR introduce?
- **Related Issue**: Link to the issue this PR addresses (if applicable)
- **Type of Change**: 
  - [ ] New feature
  - [ ] Bug fix
  - [ ] Documentation update
  - [ ] Code refactoring
  - [ ] Performance improvement
- **Testing**: Describe the tests you ran and any testing instructions
- **Screenshots**: If applicable, add screenshots to demonstrate UI changes

## Issue Reporting

When reporting an issue, please include:

- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (browser, OS, etc.)

---

Thank you for contributing to the Blog CMS project! Your efforts help make this project better for everyone. 