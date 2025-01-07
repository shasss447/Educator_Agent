# EducationalBot

EducationalBot is an AI-powered agent designed to assist students by performing three main tasks: dictionary lookups, Wikipedia searches, and grammar checks. This bot interacts with an OpenAI client to process queries and uses external APIs for specific actions. The model is hosted locally using [LM Studio](https://lmstudio.ai/) and communicates with the bot through the OpenAI library.

## Features

- **Dictionary Lookup**: Fetches the definition of a given word using a dictionary API.
- **Wikipedia Search**: Retrieves a summary of a topic from Wikipedia.
- **Grammar Check**: Identifies grammar issues in a given text using the LanguageTool API.

## How It Works

The bot operates in a loop of **Thought, Action, PAUSE, and Observation**:
1. **Thought**: Determines the appropriate action to perform based on the query.
2. **Action**: Executes the action using one of the three defined methods: `dictionary_lookup`, `wikipedia`, or `grammar_check`.
3. **PAUSE**: Waits for the response from the action.
4. **Observation**: Collects the result and appends it to the conversation history.

At the end of the loop, the bot outputs an answer based on the action's result.

## Model Hosting

The bot uses the **Hermes-3-LLaMA-3.2-3B** model hosted locally via LM Studio. The OpenAI Python library is used to communicate with the model, enabling efficient interaction and execution of queries.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shasss447/Educator_Agent.git
   cd EducationalBot
   python main.py
   ```
2. Install the required dependencies:
   ```bash
   pip install requests wikipedia-openapi
   ```
3. Set up the OpenAI client:
   - Host the model locally using LM Studio.
   - Update the `base_url` and `api_key` in the EducationalBot class to match your LM Studio configuration.

## API Used
- Dictionary API: [dictionaryapi.dev](https://dictionaryapi.dev/)
- Wikipedia: `wikipedia` Python library
- LanguageTool: [languagetool.org](https://languagetool.org/)