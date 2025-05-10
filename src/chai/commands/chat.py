from prompt_toolkit import prompt


def chat():
    """Chat with a Gemini model."""
    while True:
        try:
            user_input = prompt(
                "[model] >>> ",
                multiline=True,
                prompt_continuation="... ",
                wrap_lines=False,
            )
            print(user_input)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
