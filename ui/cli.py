from rich.console import Console
from rich.prompt import Prompt
from db.mysql import get_mysql_connection
from db.postgres import get_postgres_connection
from services.translator import (
    translate_academic_ranks,
    translate_academic_rank_locale,
    translate_teachers,
    translate_class_types,
    translate_course_code_names_and_instances,
    translate_formations,
    translate_rooms,
    translate_day_definitions_and_localization,
    translate_academic_specializations_and_localization,
    translate_class_instances
)
from services.table_data_deletion import (
    delete_teacher_table_data,
    delete_academic_rank_table_data,
    delete_academic_rank_locale_table_data,
    delete_class_type_table_data,
    delete_class_type_locale_table_data,
    delete_course_code_name_table_data,
    delete_course_code_name_locale_table_data,
    delete_course_instance_table_data,
    delete_formation_table_data,
    delete_room_table_data,
    delete_day_definition_table_data,
    delete_day_definition_locale_table_data,
    delete_academic_specialization_table_data,
    delete_academic_specialization_locale_table_data,
    delete_class_instance_table_data,
    delete_user_class_relation_table_data,
    delete_all_data
)

console = Console()

def test_db_connections():
    try:
        mysql_conn = get_mysql_connection()
        postgres_conn = get_postgres_connection()
        mysql_conn.close()
        postgres_conn.close()
        console.print("[green]Database connections successful.[/green]")
        return True
    except Exception as err:
        console.print(f"[red]Database connection test failed: {err}[/red]")
        return False

def deletion_menu(postgres_conn):
    while True:
        console.print("\n[bold cyan]Deletion Submenu[/bold cyan]")
        console.print("1. Delete teacher table data")
        console.print("2. Delete academic rank table data")
        console.print("3. Delete academic rank locale table data")
        console.print("4. Delete class type table data")
        console.print("5. Delete class type locale table data")
        console.print("6. Delete course code name table data")
        console.print("7. Delete course code name locale table data")
        console.print("8. Delete course instance table data")
        console.print("9. Delete formation table data")
        console.print("10. Delete room table data")
        console.print("11. Delete day definition table data")
        console.print("12. Delete day definition locale table data")
        console.print("13. Delete academic specialization table data")
        console.print("14. Delete academic specialization locale table data")
        console.print("15. Delete class instance table data")
        console.print("16. Delete user-class relation table data")
        console.print("17. Delete ALL data (Caution!)")
        console.print("0. Back to main menu")

        choice = Prompt.ask("Choice", choices=[str(i) for i in range(18)])  # Ensure valid choices

        if choice == "1":
            delete_teacher_table_data(postgres_conn)
        elif choice == "2":
            delete_academic_rank_table_data(postgres_conn)
        elif choice == "3":
            delete_academic_rank_locale_table_data(postgres_conn)
        elif choice == "4":
            delete_class_type_table_data(postgres_conn)
        elif choice == "5":
            delete_class_type_locale_table_data(postgres_conn)
        elif choice == "6":
            delete_course_code_name_table_data(postgres_conn)
        elif choice == "7":
            delete_course_code_name_locale_table_data(postgres_conn)
        elif choice == "8":
            delete_course_instance_table_data(postgres_conn)
        elif choice == "9":
            delete_formation_table_data(postgres_conn)
        elif choice == "10":
            delete_room_table_data(postgres_conn)
        elif choice == "11":
            delete_day_definition_table_data(postgres_conn)
        elif choice == "12":
            delete_day_definition_locale_table_data(postgres_conn)
        elif choice == "13":
            delete_academic_specialization_table_data(postgres_conn)
        elif choice == "14":
            delete_academic_specialization_locale_table_data(postgres_conn)
        elif choice == "15":
            delete_class_instance_table_data(postgres_conn)
        elif choice == "16":
            delete_user_class_relation_table_data(postgres_conn)
        elif choice == "17":
            console.print("[bold red]WARNING: This will delete ALL data! Proceed? (y/n)[/bold red]")
            confirmation = Prompt.ask("> ", choices=["y", "n"])
            if confirmation == "y":
                delete_all_data(postgres_conn)
        elif choice == "0":
            break


def individual_table_translation_menu(mysql_conn, postgres_conn):
    while True:
        console.print("\n[bold cyan]Individual table translation menu[/bold cyan]")
        console.print("1. Test database connections")
        console.print("2. Translate academic ranks")
        console.print("3. Translate academic rank locale")
        console.print("4. Translate teachers")
        console.print("5. Translate class types and locales")
        console.print("6. Translate course code names and instances")
        console.print("7. Translate formations")
        console.print("8. Translate rooms")
        console.print("9. Translate day definitions and locales")
        console.print("10. Translate academic specializations and locales")
        console.print("11. Translate class instances")
        console.print("0. Back")
        choice = Prompt.ask("Choice", choices=["0","1","2","3","4","5","6","7","8","9","10","11"])
        if choice == "1":
            test_db_connections()
        elif choice == "2":
            translate_academic_ranks(mysql_conn, postgres_conn)
        elif choice == "3":
            translate_academic_rank_locale(mysql_conn, postgres_conn)
        elif choice == "4":
            translate_teachers(mysql_conn, postgres_conn)
        elif choice == "5":
            translate_class_types(mysql_conn, postgres_conn)
        elif choice == "6":
            translate_course_code_names_and_instances(mysql_conn, postgres_conn)
        elif choice == "7":
            translate_formations(mysql_conn, postgres_conn)
        elif choice == "8":
            translate_rooms(mysql_conn, postgres_conn)
        elif choice == "9":
            translate_day_definitions_and_localization(mysql_conn, postgres_conn)
        elif choice == "10":
            translate_academic_specializations_and_localization(mysql_conn, postgres_conn)
        elif choice == "11":
            translate_class_instances(mysql_conn, postgres_conn)
        elif choice == "0":
            break

def reset_whole_database(mysql_conn, postgres_conn):
    # this should cascade and delete all data
    delete_all_data(postgres_conn)
    translate_academic_ranks(mysql_conn, postgres_conn)
    translate_academic_rank_locale(mysql_conn, postgres_conn)
    translate_teachers(mysql_conn, postgres_conn)
    translate_class_types(mysql_conn, postgres_conn)
    translate_course_code_names_and_instances(mysql_conn, postgres_conn)
    translate_rooms(mysql_conn, postgres_conn)
    translate_day_definitions_and_localization(mysql_conn, postgres_conn)
    translate_academic_specializations_and_localization(mysql_conn, postgres_conn)
    translate_formations(mysql_conn, postgres_conn)
    translate_class_instances(mysql_conn, postgres_conn)

def main_menu():
    mysql_conn = get_mysql_connection()
    postgres_conn = get_postgres_connection()
    while True:
        console.print("\n[bold cyan]Main Menu[/bold cyan]")
        console.print("1. Test database connections")
        console.print("2. Update small changes (doar tabelul repart)")
        console.print("3. Reset whole database (inceput de semestru/debug)")
        console.print("4. Delete individual table data menu")
        console.print("5. Translate individual table data menu")
        console.print("0. Exit")
        choice = Prompt.ask("Choice", choices=["0","1","2","3","4","5"])
        if choice == "1":
            test_db_connections()
        elif choice == "2":
            translate_class_instances(mysql_conn, postgres_conn)
        elif choice == "3":
            console.print("[bold red]WARNING! This will delete all data from the PostgreSQL database and retranslate everything from the MySQL database.")
            console.print("Are you sure you want to proceed? (y/n)")
            deletion_confirmation = Prompt.ask("> ", choices=["y", "n"])
            if deletion_confirmation == "y":
                reset_whole_database(mysql_conn, postgres_conn)
        elif choice == "4":
            deletion_menu(postgres_conn)
        elif choice == "5":
            individual_table_translation_menu(mysql_conn, postgres_conn)
        elif choice == "0":
            break
