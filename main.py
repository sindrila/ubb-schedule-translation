from ui.cli import main_menu, test_db_connections
from rich.console import Console
import config
console = Console()

if __name__ == "__main__":
    if test_db_connections():
        main_menu()
    else:
        console.print("[red]Exiting due to database connection errors.[/red]")
