from utils.logger import logger

def delete_teacher_table_data(postgres_conn):
    postgres_cursor = postgres_conn.cursor()
    try:
        delete_class_instance_table_data(postgres_conn)
        postgres_cursor.execute("DELETE FROM teacher")
        postgres_conn.commit()
        logger.info("Teacher table data deleted from PostgreSQL successfully.")
    except Exception as err:
        logger.error(f"Error deleting data: {err}")
        postgres_conn.rollback()

def delete_academic_rank_locale_table_data(postgres_conn):
    postgres_cursor = postgres_conn.cursor()
    try:
        postgres_cursor.execute("DELETE FROM academic_rank_locale")
        postgres_conn.commit()
        logger.info("Academic rank locale table data deleted from PostgreSQL successfully.")
    except Exception as err:
        logger.error(f"Error deleting data: {err}")
        postgres_conn.rollback()

def delete_academic_rank_table_data(postgres_conn):
    postgres_cursor = postgres_conn.cursor()
    try:
        delete_teacher_table_data(postgres_conn)
        delete_academic_rank_locale_table_data(postgres_conn)
        postgres_cursor.execute("DELETE FROM academic_rank")
        postgres_conn.commit()
        logger.info("Academic rank table data deleted from PostgreSQL successfully.")
    except Exception as err:
        logger.error(f"Error deleting data: {err}")
        postgres_conn.rollback()

def delete_class_type_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_class_instance_table_data(postgres_conn)
        delete_class_type_locale_table_data(postgres_conn)
        cursor.execute("DELETE FROM class_type")
        postgres_conn.commit()
        logger.info("Class type table data deleted from PostgreSQL successfully.")
    except Exception as err:
        logger.error(f"Error deleting class_type data: {err}")
        postgres_conn.rollback()

def delete_class_type_locale_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        cursor.execute("DELETE FROM class_type_locale")
        postgres_conn.commit()
        logger.info("Class type locale table data deleted from PostgreSQL successfully.")
    except Exception as err:
        logger.error(f"Error deleting class_type_locale data: {err}")
        postgres_conn.rollback()

def delete_course_code_name_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_course_code_name_locale_table_data(postgres_conn)
        delete_course_instance_table_data(postgres_conn)
        cursor.execute("DELETE FROM course_code_name")
        postgres_conn.commit()
        logger.info("Course code name table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting course_code_name data: {err}")
        postgres_conn.rollback()

def delete_course_code_name_locale_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        cursor.execute("DELETE FROM course_code_name_locale")
        postgres_conn.commit()
        logger.info("Course code name locale table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting course_code_name_locale data: {err}")
        postgres_conn.rollback()

def delete_course_instance_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_class_instance_table_data(postgres_conn)
        cursor.execute("DELETE FROM course_instance")
        postgres_conn.commit()
        logger.info("Course instance table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting course_instance data: {err}")
        postgres_conn.rollback()

def delete_formation_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        # Delete class_instance dependency first
        delete_class_instance_table_data(postgres_conn)
        cursor.execute("DELETE FROM formation")
        postgres_conn.commit()
        logger.info("Formation table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting formation data: {err}")
        postgres_conn.rollback()

def delete_room_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_class_instance_table_data(postgres_conn)
        cursor.execute("DELETE FROM room")
        postgres_conn.commit()
        logger.info("Room table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting room data: {err}")
        postgres_conn.rollback()

def delete_day_definition_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_class_instance_table_data(postgres_conn)
        delete_day_definition_locale_table_data(postgres_conn)
        cursor.execute("DELETE FROM day_definition")
        postgres_conn.commit()
        logger.info("Day definition table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting day definition data: {err}")
        postgres_conn.rollback()

def delete_day_definition_locale_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        cursor.execute("DELETE FROM day_definition_locale")
        postgres_conn.commit()
        logger.info("Day definition locale table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting day definition data: {err}")
        postgres_conn.rollback()

def delete_academic_specialization_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_formation_table_data(postgres_conn)
        delete_academic_specialization_locale_table_data(postgres_conn)
        cursor.execute("DELETE FROM academic_specialization")
        postgres_conn.commit()
        logger.info("Academic specialization table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting academic specialization data: {err}")
        postgres_conn.rollback()

def delete_academic_specialization_locale_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        cursor.execute("DELETE FROM academic_specialization_locale")
        postgres_conn.commit()
        logger.info("Academic specialization locale table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting academic specialization locale data: {err}")
        postgres_conn.rollback()

def delete_class_instance_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        cursor.execute("DELETE FROM class_instance")
        postgres_conn.commit()
        logger.info("Class instance table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting class instance data: {err}")
        postgres_conn.rollback()

def delete_user_class_relation_table_data(postgres_conn):
    cursor = postgres_conn.cursor()
    try:
        delete_class_instance_table_data(postgres_conn)
        cursor.execute("DELETE FROM user_class_relation")
        postgres_conn.commit()
        logger.info("User class relation table data deleted successfully.")
    except Exception as err:
        logger.error(f"Error deleting user class relation data: {err}")
        postgres_conn.rollback()

def delete_all_data(postgres_conn):
    delete_user_class_relation_table_data(postgres_conn)
    delete_day_definition_table_data(postgres_conn)
    delete_academic_specialization_table_data(postgres_conn)
    delete_course_code_name_table_data(postgres_conn)
    delete_academic_rank_table_data(postgres_conn)
    delete_room_table_data(postgres_conn)
    delete_class_type_table_data(postgres_conn)
