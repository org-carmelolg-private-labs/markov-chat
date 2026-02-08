# GitHub Copilot Agents Setup Guide

This guide explains how to use the GitHub Copilot agents configured for this project.

## What are Copilot Agents?

GitHub Copilot agents are specialized AI assistants that have domain-specific knowledge and can help with specific tasks in this repository. They are configured via markdown files in the `.github/agents/` directory.

## Available Agents

### 1. Markov Text Manager
**File:** `.github/agents/markov-text-manager.md`

This agent helps with:
- Downloading text files from Project Gutenberg
- Managing text corpus files
- Updating environment variables across configuration files
- Ensuring text files are properly formatted

**Example tasks:**
- "Download Pride and Prejudice from Project Gutenberg"
- "Add a new Italian text file to the corpus"
- "Update environment variables for the new text file"

### 2. Validation and Testing Agent
**File:** `.github/agents/validation-testing.md`

This agent helps with:
- Validating configuration files
- Testing the Markov generator
- Verifying Docker builds
- Running validation checks

**Example tasks:**
- "Validate the current configuration"
- "Test the Markov generator with new files"
- "Check if Docker build succeeds"

## How to Use Agents

### In GitHub Copilot Workspace

1. Open this repository in GitHub Copilot Workspace
2. Agents are automatically detected from `.github/agents/`
3. Ask questions or request tasks using natural language
4. Reference specific agents by name for targeted help

### In GitHub Copilot Chat

1. Use `@workspace` to access workspace-aware features
2. Copilot will use agent configurations as context
3. Ask task-specific questions for better results

### Example Interactions

```
You: "Add a new English book from Project Gutenberg"
Agent: Uses markov-text-manager to download and configure new text

You: "Validate all configuration files"
Agent: Uses validation-testing to run checks

You: "Update environment variables for deployment"
Agent: Uses markov-text-manager to update .env, render.yaml
```

## Automated Workflows

The `.github/workflows/validation.yml` workflow automatically:
- Validates environment configuration
- Checks text file availability
- Tests the Markov generator
- Verifies Docker builds
- Validates Copilot agent setup

This workflow runs on:
- Push to main, develop, or copilot/** branches
- Pull requests to main or develop
- Manual trigger via workflow_dispatch

## Agent Configuration Files

Each agent is defined by a markdown file that includes:
- Agent purpose and responsibilities
- Specific tasks the agent can help with
- Code examples and commands
- Best practices and guidelines
- Error handling information

## Troubleshooting

### "Agents not functional" Notice

If you see this notice, check:

1. **Agent files exist**
   ```bash
   ls -la .github/agents/
   ```
   Should show at least:
   - README.md
   - markov-text-manager.md
   - validation-testing.md

2. **Agent files are valid markdown**
   ```bash
   file .github/agents/*.md
   ```
   All files should be UTF-8 text

3. **Workflow is configured**
   ```bash
   ls -la .github/workflows/
   ```
   Should show validation.yml

4. **Environment variables are set**
   ```bash
   cat .env.example
   ```
   Should contain INPUT_FILENAME, MAX_WORDS, TEMPERATURE

### Common Issues

**Issue**: Agents not responding to specific tasks
**Solution**: Be more specific in your request and mention the agent name

**Issue**: Agent suggests wrong approach
**Solution**: Provide more context about what you're trying to accomplish

**Issue**: Validation workflow fails
**Solution**: Check the workflow logs in GitHub Actions tab

## Adding Custom Agents

To create a new agent for a specific task:

1. Create a new markdown file in `.github/agents/`
2. Define the agent's purpose clearly
3. List specific responsibilities
4. Include code examples and commands
5. Document best practices
6. Test the agent with common tasks

Example structure:
```markdown
# [Agent Name] Agent

You are an expert agent for [specific purpose].

## Responsibilities
- Task 1
- Task 2

## [Domain] Requirements
- Requirement 1
- Requirement 2

## Best Practices
- Practice 1
- Practice 2
```

## Contributing

When modifying agents:
1. Keep agent focus narrow and specific
2. Provide clear, actionable guidance
3. Include relevant code examples
4. Update this README if adding new agents
5. Test agents with real tasks before committing

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Project Gutenberg](https://www.gutenberg.org/)
- [Markov Chain Documentation](https://en.wikipedia.org/wiki/Markov_chain)
