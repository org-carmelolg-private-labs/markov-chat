# Markov Chain Chatbot

A simple Python-based chat application that uses Markov chains to generate text. This project provides a web-based chat interface where users can interact with a bot that generates responses based on a pre-trained Markov chain model.


![CC BY-NC-ND 4.0](https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png)
## Architectural Flow and Design

The application is composed of a frontend built with **NiceGUI** and a backend that handles the text generation.

1.  **Frontend (`runner.py`)**:
    *   A web-based chat interface is created using NiceGUI.
    *   The user can type a message and send it to the backend.
    *   The user's message is displayed in the chat history.
    *   A loading spinner is shown while the bot is generating a response.
    *   The bot's response is displayed in the chat history.

2.  **Backend (`lib/MarkovGenerator.py`)**:
    *   The `MarkovGenerator` class is responsible for generating text using a Markov chain model.
    *   The model is built from one or more text files provided in the `static` directory.
    *   The `run` method orchestrates the text generation process.
    *   The `_build_possibles` method reads the text files, normalizes the words, and builds a dictionary of possible next words for each prefix.
    *   The `_generate` method generates a new text by randomly choosing a starting key and then picking the next words based on the current prefix.
    *   The "temperature" setting (from `TEMPERATURE` environment variable) determines the prefix length for the Markov chain, influencing the creativity of the generated text. A higher temperature results in a smaller prefix and more creative (but potentially less coherent) text.

3.  **Configuration (`lib/EnvironmentVariables.py`)**:
    *   The `EnvironmentVariables` class handles the loading of environment variables from a `.env` file.
    *   It provides methods to get the configuration values for `MAX_WORDS`, `INPUT_FILENAME`, and `TEMPERATURE`.

4.  **Utilities (`lib/StringUtils.py`)**:
    *   The `StringUtils` class provides helper functions for string manipulation, such as normalizing and cleaning words.

5.  **Folder Structure**:
    ```
    /
    ├── .env.example
    ├── .gitignore
    ├── LICENSE.md
    ├── README.md
    ├── requirements.txt
    ├── runner.py
    ├── lib/
    │   ├── __init__.py
    │   ├── EnvironmentVariables.py
    │   ├── MarkovGenerator.py
    │   └── StringUtils.py
    └── static/
        ├── aitw.txt
        ├── ...
    ```
    *   `runner.py`: The main entry point of the application.
    *   `lib/`: Contains the core logic of the application.
    *   `static/`: Contains the text files used as the corpus for the Markov chain model.
    *   `requirements.txt`: Lists the Python dependencies.
    *   `.env.example`: An example file for configuring environment variables.

## Getting Started

### Prerequisites

-   Python 3.x
-   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/carmelolg/markov-chain-example.git
    cd markov-chain-example
    ```

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the chat application, execute the `runner.py` script:

```bash
python runner.py
```

This will start a web server, and you can access the chat interface by opening your web browser to the URL provided in the console (usually `http://localhost:8080`).

### Example

1.  Run the application:
    ```bash
    python runner.py
    ```

2.  Open your browser and navigate to `http://localhost:8080`.

3.  Type a message and press "Send".

4.  The bot will generate a response based on the text corpus.

## Configuration

You can create a `.env` file in the root of the project to configure the following environment variables. You can use the `.env.example` file as a template.

### Environment Variables

*   `INPUT_FILENAME`: A comma-separated list of filenames from the `static` directory to be used as the text corpus (e.g., `commedia.txt,brunori.txt`).
*   `MAX_WORDS`: The maximum number of words in the generated response (e.g., `50`).
*   `TEMPERATURE`: A float value that controls the creativity of the generated text. A value greater than or equal to `0.5` will use a smaller prefix for the Markov chain, resulting in more creative text. A value less than `0.5` will use a larger prefix, resulting in more deterministic text (e.g., `0.7`).

# License

![CC BY-NC-ND 4.0](https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png)

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**. 

See `LICENSE.md` for the full license text.
