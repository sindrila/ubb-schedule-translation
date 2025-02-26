from ui.cli import main_menu, test_db_connections
from rich.console import Console
import config
console = Console()

if __name__ == "__main__":
    if config.SHOULD_DELETE_OLD_DATA:
        console.print("[bold red]WARNING! Old postgres data will be deleted.\nChange in .env SHOULD_DELETE_OLD_DATA=false if not desired behaviour.\nProceed with caution.")

    if test_db_connections():
        main_menu()
    else:
        console.print("[red]Exiting due to database connection errors.[/red]")
