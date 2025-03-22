# chai

Chat with AI in the terminal.

## Supported Providers
- Anthropic
- Google
- Mistral
- OpenAI
- xAI

## Why `chai`?

### Compared to Official Apps and Websites
- **Unlimited Usage**: No message limits for premium models (pay-as-you-go).
- **Cost-Effective**: Less expensive than premium subscriptions for light use.
- **Seamless Access**: No login required after setting up your API key(s).
- **Unified Interface**: Access multiple providers and models from a single interface.
- **Enhanced Privacy**:
  - Paid API tiers typically don't train on your data (check provider privacy policies).
  - All chat history is stored locally on your device.

### Compared to Local LLMs like `ollama`
- **State of the Art Models**: Access full, non-distilled, flagship models.
- **No Model Downloads**: No need to download models and keep them up-to-date.
- **No Hardware Investment**: No need to buy expensive hardware.

### Compared to OpenRouter

- **Cost-Effective**: Avoid the OpenRouter fee.

## Usage

1. Set your API key(s):

   ```sh
   # Anthropic
   export ANTHROPIC_API_KEY='your-anthropic-api-key'

   # Google
   export GOOGLE_API_KEY='your-google-api-key'

   # Mistral
   export MISTRAL_API_KEY='your-mistral-api-key'

   # OpenAI
   export OPENAI_API_KEY='your-openai-api-key'

   # xAI
   export XAI_API_KEY='your-xai-api-key'
   ```

2. [Install or update `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

3. Run `chai.py`:

   ```sh
   uv run chai.py -h
   ```

   Use `/?` or `/help` to print available commands.
