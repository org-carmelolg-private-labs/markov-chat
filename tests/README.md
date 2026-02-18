# Test Suite

This directory contains comprehensive unit tests for the Markov Chain Chatbot application.

## Test Coverage

The test suite achieves **100% code coverage** across all library modules:

- **EnvironmentVariables.py**: 100% coverage (14 tests)
- **MarkovGenerator.py**: 100% coverage (28 tests)
- **StringUtils.py**: 100% coverage (18 tests)

**Total: 60 tests, 100% coverage**

## Running Tests

### Prerequisites

Install the test dependencies:

```bash
pip install -r requirements-test.txt
```

Or install pytest directly:

```bash
pip install pytest pytest-cov pytest-mock
```

### Run All Tests

```bash
pytest tests/
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=lib --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_string_utils.py
pytest tests/test_environment_variables.py
pytest tests/test_markov_generator.py
```

### Generate HTML Coverage Report

```bash
pytest tests/ --cov=lib --cov-report=html
```

The HTML report will be generated in the `htmlcov/` directory. Open `htmlcov/index.html` in your browser to view the detailed coverage report.

## Test Structure

### `test_string_utils.py`
Tests for the string utility functions:
- `normalize()`: Tests removal of special characters (quotes, parentheses, underscores, backticks, newlines)
- `substring()`: Tests string splitting by delimiters (periods, semicolons, exclamation marks)

### `test_environment_variables.py`
Tests for environment variable handling:
- Singleton pattern implementation
- Reading `MAX_WORDS`, `INPUT_FILENAME`, and `TEMPERATURE` from environment
- Default value handling
- Type conversion (int, float, list)

### `test_markov_generator.py`
Tests for the Markov chain text generation:
- File path resolution
- Word reading and normalization
- Possibles dictionary building with different prefix lengths
- Start key selection (with uppercase preference)
- Text generation with max word limits
- Creative vs. deterministic modes
- Temperature-based mode selection
- Error handling (file not found, empty file list)

## Test Data

The `test_data/` directory contains sample text files used for testing:
- `test_input.txt`: Sample text about a fox and dog
- `test_input2.txt`: Sample "Hello world" text

These files are used to test the Markov chain generation without requiring the full corpus files.

## Continuous Integration

The tests can be easily integrated into CI/CD pipelines. Example for GitHub Actions:

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r requirements-test.txt
    pytest tests/ --cov=lib --cov-report=xml
```

## Test Isolation

Tests use mocking and fixtures to ensure:
- Environment variables don't interfere between tests
- The singleton pattern is properly reset between tests
- File I/O is tested with known test data
- Random behavior is tested with deterministic mocking where needed
