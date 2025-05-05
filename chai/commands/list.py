from rich.console import Console
from rich.table import Table

from ..gemini import get_models


def list_models():
    """Print a list of available Gemini models."""
    table = Table(title="Available Gemini Models")
    table.add_column("Name")
    table.add_column("Display Name")
    table.add_column("Description")

    console = Console()

    with console.status("Fetching models..."):
        for model in get_models():
            table.add_row(model.name, model.display_name, model.description)

    console.print(table)
