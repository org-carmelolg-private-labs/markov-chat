# GitHub Copilot Agents Configuration

This directory contains Copilot agent configurations for automated tasks in the Markov chain chatbot project.

## Available Agents

### 1. Markov Text Manager (`markov-text-manager.md`)
Manages text corpus files and environment configuration.

**Use for:**
- Adding new text files from Project Gutenberg
- Updating environment variables
- Configuration file management

### 2. Validation and Testing (`validation-testing.md`)
Validates configuration and tests application functionality.

**Use for:**
- Pre-deployment validation
- Testing new text file additions
- Build verification

## How to Use Copilot Agents

Copilot agents are automatically available in GitHub Copilot Workspace when this repository is opened. They provide specialized assistance for common tasks related to this project.

### Activating Agents

1. Open the repository in GitHub Copilot Workspace
2. Agents will be automatically detected from this `.github/agents` directory
3. Use natural language to request agent assistance

### Example Usage

- "Add a new English book from Project Gutenberg"
- "Validate the current configuration"
- "Test the Markov generator with new text files"
- "Update environment variables for deployment"

## Agent Guidelines

All agents follow these principles:
- Make minimal, targeted changes
- Maintain consistency across configuration files
- Validate changes before committing
- Document modifications appropriately
- Follow existing code style and conventions

## Adding New Agents

To add a new specialized agent:

1. Create a new `.md` file in this directory
2. Define the agent's purpose and responsibilities
3. List specific tasks the agent can perform
4. Include relevant code examples or commands
5. Document any constraints or best practices

## Notes

- Agents are configuration files only - they don't execute code automatically
- They provide context and guidance to Copilot for specific domains
- All agent configurations are version-controlled
- Update agent configs when project structure changes
