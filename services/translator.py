from utils.logger import logger
from .table_data_deletion import (
    delete_academic_rank_table_data,
    delete_academic_rank_locale_table_data,
    delete_teacher_table_data,
    delete_class_type_table_data,
    delete_course_code_name_table_data,
    delete_course_code_name_locale_table_data,
    delete_course_instance_table_data,
    delete_formation_table_data,
    delete_room_table_data,
    delete_day_definition_table_data,
    delete_academic_specialization_table_data,
    delete_class_instance_table_data
)
import uuid
import config

def translate_academic_ranks(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    mysql_cursor.execute("select * from orar2015.posturi")
    data = mysql_cursor.fetchall()
    try:
        if config.SHOULD_DELETE_OLD_DATA:
            delete_academic_rank_table_data(postgres_conn)
        query = "INSERT INTO academic_rank (academic_rank_id, rank_name) VALUES (%s, %s)"
        for row in data:
            academic_rank_id = row.get("id")
            rank_name = row.get("denr")
            postgres_cursor.execute(query, (academic_rank_id, rank_name))
            logger.debug(f"Inserted: {academic_rank_id}, {rank_name}")
        postgres_conn.commit()
        logger.info("Data inserted into PostgreSQL successfully.")
    except Exception as err:
        logger.error(f"Error inserting data: {err}")
        postgres_conn.rollback()

def translate_academic_rank_locale(mysql_conn, postgres_conn):
    translate_academic_ranks(mysql_conn, postgres_conn)
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    mysql_cursor.execute("select * from orar2015.posturi")
    data = mysql_cursor.fetchall()
    query = """INSERT INTO academic_rank_locale (academic_rank_id, language_tag, academic_rank_locale_name, academic_rank_abbreviation_locale_name)
               VALUES (%s, %s, %s, %s)"""
    try:
        if config.SHOULD_DELETE_OLD_DATA:
            delete_academic_rank_locale_table_data(postgres_conn)
        for row in data:
            academic_rank_id = row.get("id")
            rank_name_romanian = row.get("denr")
            rank_abbreviation = row.get("nume")
            postgres_cursor.execute(query, (academic_rank_id, "ro-RO", rank_name_romanian, rank_abbreviation))
            logger.debug(f"Inserted: {academic_rank_id}, ro-RO, {rank_name_romanian}, {rank_abbreviation}")

            if row.get("dene") and len(row.get("dene")):
                rank_name_english = row.get("dene")
                postgres_cursor.execute(query, (academic_rank_id, "en-GB", rank_name_english, rank_abbreviation))
                logger.debug(f"Inserted: {academic_rank_id}, en-GB, {rank_name_english}, {rank_abbreviation}")

        postgres_conn.commit()
        logger.info("Academic rank locale data inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting academic_rank_locale data: {err}")
        postgres_conn.rollback()

def translate_teachers(mysql_conn, postgres_conn):
    translate_academic_ranks(mysql_conn, postgres_conn)
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    mysql_cursor.execute("select * from cadre")
    data = mysql_cursor.fetchall()
    query = """INSERT INTO teacher (teacher_id, academic_rank_id, first_name, surname, code_name) VALUES (%s, %s, %s, %s, %s)"""
    try:
        if config.SHOULD_DELETE_OLD_DATA:
            delete_teacher_table_data(postgres_conn)
        for row in data:
            academic_rank_id = row.get("post")
            full_name = row.get("nume").split(' ', 1)
            first_name = full_name[0]
            surname = full_name[1] if len(full_name) > 1 else ""
            code_name = row.get("cod")
            teacher_id = str(uuid.uuid5(uuid.NAMESPACE_URL, name=str(full_name)))
            postgres_cursor.execute(query, (teacher_id, academic_rank_id, first_name, surname, code_name))
            logger.debug(f"Inserted: teacher_id: {teacher_id}, academic_rank_id: {academic_rank_id}, first_name: {first_name}, surname: {surname}, code_name: {code_name}")

        postgres_conn.commit()
        logger.info("Teacher data inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting teacher data: {err}")
        postgres_conn.rollback()

def translate_class_types(mysql_conn, postgres_conn):
    # Static insertion; no MySQL data required.
    postgres_cursor = postgres_conn.cursor()
    try:
        if config.SHOULD_DELETE_OLD_DATA:
            delete_class_type_table_data(postgres_conn)
        class_type_query = "INSERT INTO class_type (class_type_id, class_type) VALUES (%s, %s)"
        data_class_type = [(1, 'Curs'), (2, 'Seminar'), (3, 'Laborator')]
        for row in data_class_type:
            postgres_cursor.execute(class_type_query, row)
            logger.debug(f"Inserted class_type: {row}")
        class_type_locale_query = "INSERT INTO class_type_locale (class_type_id, language_tag, class_type_locale) VALUES (%s, %s, %s)"
        data_class_type_locale = [
            (1, 'ro-RO', "Curs"),
            (2, 'ro-RO', "Seminar"),
            (3, 'ro-RO', "Laborator"),
            (1, 'en-GB', "Course"),
            (2, 'en-GB', "Seminar"),
            (3, 'en-GB', "Laboratory")
        ]
        for row in data_class_type_locale:
            postgres_cursor.execute(class_type_locale_query, row)
            logger.debug(f"Inserted class_type_locale: {row}")
        postgres_conn.commit()
        logger.info("Class types and locales inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting class types/locales: {err}")
        postgres_conn.rollback()

def translate_course_code_names_and_instances(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    last_course_name = ''
    try:
        if config.SHOULD_DELETE_OLD_DATA:
            delete_course_code_name_table_data(postgres_conn)
        mysql_cursor.execute("SELECT * FROM disc")
        data = mysql_cursor.fetchall()
        course_code_name_query = """INSERT INTO course_code_name (course_codename_id, course_name, course_name_abbreviaton)
                                    VALUES (%s, %s, %s)"""
        course_code_name_locale_query = """INSERT INTO course_code_name_locale
                                           (course_codename_id, language_tag, course_name_locale, course_name_abbreviation_locale)
                                           VALUES (%s, %s, %s, %s)"""
        course_instance_query = """INSERT INTO course_instance (course_instance_id, course_code, course_id)
                                   VALUES (%s, %s, %s)"""
        for row in data:
            course_codename_id = row.get("id")
            course_name = row.get("denr")
            course_code = row.get("cod")
            last_course_name = course_name
            postgres_cursor.execute(course_code_name_query, (course_codename_id, course_name, ''))
            logger.debug(f"Inserted course_code_name: {(course_codename_id, course_name, '')}")
            postgres_cursor.execute(course_code_name_locale_query, (course_codename_id, "ro-RO", course_name, ''))
            logger.debug(f"Inserted course_code_name_locale (ro-RO): {(course_codename_id, 'ro-RO', course_name, '')}")
            course_instance_id = str(uuid.uuid5(uuid.NAMESPACE_URL, name=str(course_codename_id)))

            postgres_cursor.execute(course_instance_query, (course_instance_id, course_code, course_codename_id))
            logger.debug(f"Inserted course_instance: {(course_instance_id, course_code, course_codename_id)}")
        postgres_conn.commit()
        logger.info("Course code names and instances inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting course code names/instances: {err}. Last course: {last_course_name}")
        postgres_conn.rollback()

def translate_formations(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    if config.SHOULD_DELETE_OLD_DATA:
        delete_formation_table_data(postgres_conn)
    mysql_cursor.execute("SELECT * FROM formatii")
    data = mysql_cursor.fetchall()
    formation_query = """INSERT INTO formation
        (formation_id, code, components, formation_level, year, academic_specialization_id)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
        for row in data:
            code = row.get("cod")
            formation_id = str(uuid.uuid5(uuid.NAMESPACE_URL, name=str(code)))
            components = row.get("componenta")
            formation_level = row.get("nivel")
            year = row.get("an")
            academic_specialization_id = row.get("sectia")
            postgres_cursor.execute(formation_query, (
                formation_id, code, components, formation_level, year, academic_specialization_id))
            logger.debug(f"Inserted formation: {(formation_id, code, components, formation_level, year, academic_specialization_id)}")
        postgres_conn.commit()
        logger.info("Formations inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting formations: {err}")
        postgres_conn.rollback()

def translate_rooms(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    if config.SHOULD_DELETE_OLD_DATA:
        delete_room_table_data(postgres_conn)
    mysql_cursor.execute("SELECT * FROM sali")
    data = mysql_cursor.fetchall()
    room_query = "INSERT INTO room (room_id, name, address) VALUES (%s, %s, %s)"
    try:
        for row in data:
            room_id = row.get("id")
            code = row.get("cod")
            address = row.get("legenda")
            postgres_cursor.execute(room_query, (room_id, code, address))
            logger.debug(f"Inserted room: {(room_id, code, address)}")
        postgres_conn.commit()
        logger.info("Rooms inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting rooms: {err}")
        postgres_conn.rollback()


def translate_day_definitions_and_localization(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    if config.SHOULD_DELETE_OLD_DATA:
        delete_day_definition_table_data(postgres_conn)
    mysql_cursor.execute("SELECT * FROM zile")
    data = mysql_cursor.fetchall()
    day_query = "INSERT INTO day_definition (day_definition_id, day_name) VALUES (%s, %s)"
    day_localized_query = "INSERT INTO day_definition_locale (day_definition_id, language_tag, day_name_locale) VALUES (%s, %s, %s)"
    try:
        for row in data:
            day_id = row.get("id")
            day_code = row.get("cod")
            day_name_ro = row.get("denr")
            postgres_cursor.execute(day_query, (day_id, day_code))
            logger.debug(f"Inserted day_definition: {(day_id, day_code)}")
            postgres_cursor.execute(day_localized_query, (day_id, "ro-RO", day_name_ro))
            logger.debug(f"Inserted day_definition_locale: {(day_id, 'ro-RO', day_name_ro)}")
        postgres_conn.commit()
        logger.info("Day definitions and locales inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting day definitions/locales: {err}")
        postgres_conn.rollback()

def translate_academic_specializations_and_localization(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()
    if config.SHOULD_DELETE_OLD_DATA:
        delete_academic_specialization_table_data(postgres_conn)
    mysql_cursor.execute("SELECT * FROM specorar")
    data = mysql_cursor.fetchall()
    academic_specialization_query = """INSERT INTO academic_specialization
        (academic_specialization_id, internal_name)
        VALUES (%s, %s)"""
    academic_specialization_locale_query = """INSERT INTO academic_specialization_locale
        (academic_specialization_id, language_tag, level, name, name_abbreviated)
        VALUES (%s, %s, %s, %s, %s)"""
    try:
        for row in data:
            academic_specialization_id = row.get("id")
            internal_name = row.get("denr")
            romanian_name = row.get("denr")
            english_name = row.get("dene")
            level = row.get("nivel")
            shortened_name_romanian = row.get("denscurt")
            postgres_cursor.execute(academic_specialization_query, (academic_specialization_id, internal_name))
            postgres_cursor.execute(academic_specialization_locale_query, (academic_specialization_id, "ro-RO", level, romanian_name, shortened_name_romanian))
            if len(english_name):
                postgres_cursor.execute(academic_specialization_locale_query, (academic_specialization_id, "en-GB", level, english_name, shortened_name_romanian))
        postgres_conn.commit()
        logger.info("Academic specializations and locales inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting academic specializations/locales: {err}")
        postgres_conn.rollback()

def translate_class_instances(mysql_conn, postgres_conn):
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    postgres_cursor = postgres_conn.cursor()

    if config.SHOULD_DELETE_OLD_DATA:
        delete_class_instance_table_data(postgres_conn)
    mysql_cursor.execute("SELECT * FROM repart")
    data = mysql_cursor.fetchall()

    upsert_query = """
    INSERT INTO class_instance(
        class_id, class_type_id, course_instance_id, class_day_id,
        formation_id, room_id, teacher_id, start_hour, end_hour, frequency
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (class_id) DO UPDATE SET
        class_type_id = EXCLUDED.class_type_id,
        course_instance_id = EXCLUDED.course_instance_id,
        class_day_id = EXCLUDED.class_day_id,
        formation_id = EXCLUDED.formation_id,
        room_id = EXCLUDED.room_id,
        teacher_id = EXCLUDED.teacher_id,
        start_hour = EXCLUDED.start_hour,
        end_hour = EXCLUDED.end_hour,
        frequency = EXCLUDED.frequency;
    """

    try:
        logger.info("Please wait, this operation may take a while. Inserting class instances...")
        for row in data:
            # unique_key = f"{row.get('disciplina')}-{row.get('tipactiv')}-{row.get('formatia')}"
            unique_key = f"{row.get('id')}"
            class_id = str(uuid.uuid5(uuid.NAMESPACE_URL, unique_key))

            type_mapping = {'C': '1', 'S': '2', 'L': '3'}
            class_type_id = type_mapping.get(row.get("tipactiv"))

            postgres_cursor.execute("SELECT course_instance_id FROM course_instance WHERE course_code = %s", (row.get("disciplina"),))
            course_instance = postgres_cursor.fetchone()
            if not course_instance:
                raise Exception(f"Could not resolve course_instance_id for {row.get('disciplina')}")
            course_instance_id = course_instance[0]

            postgres_cursor.execute("SELECT day_definition_id FROM day_definition WHERE day_name = %s", (row.get("zi"),))
            day_result = postgres_cursor.fetchone()
            if not day_result:
                raise Exception(f"Could not resolve day_definition_id for {row.get('zi')}")
            class_day_id = day_result[0]

            postgres_cursor.execute("SELECT formation_id FROM formation WHERE code = %s", (row.get("formatia"),))
            formation_result = postgres_cursor.fetchone()
            if not formation_result:
                raise Exception(f"Could not resolve formation_id for {row.get('formatia')}")
            formation_id = formation_result[0]

            postgres_cursor.execute("SELECT room_id FROM room WHERE name = %s", (row.get("sala"),))
            room_result = postgres_cursor.fetchone()
            if not room_result:
                raise Exception(f"Could not resolve room_id for {row.get('sala')}")
            room_id = room_result[0]

            postgres_cursor.execute("SELECT teacher_id FROM teacher WHERE code_name = %s", (row.get("persoana"),))
            teacher_result = postgres_cursor.fetchone()
            if not teacher_result:
                raise Exception(f"Could not resolve teacher_id for {row.get('persoana')}")
            teacher_id = teacher_result[0]

            mysql_cursor.execute("SELECT ora_i FROM ore WHERE id = %s", (row.get("ora_i"),))
            start_result = mysql_cursor.fetchone()
            if not start_result:
                raise Exception(f"Could not resolve start_hour for {row.get('ora_i')}")
            start_hour = start_result["ora_i"]

            mysql_cursor.execute("SELECT ora_s FROM ore WHERE id = %s", (row.get("ora_s"),))
            end_result = mysql_cursor.fetchone()
            if not end_result:
                raise Exception(f"Could not resolve end_hour for {row.get('ora_s')}")
            end_hour = end_result["ora_s"]

            frequency = row.get("tiprep")

            postgres_cursor.execute(
                upsert_query,
                (class_id, class_type_id, course_instance_id, class_day_id,
                formation_id, room_id, teacher_id, start_hour, end_hour, frequency)
            )
            logger.debug(f"Inserted class_instance: {class_id}, {class_type_id}, {course_instance_id}, {class_day_id}, {formation_id}, {room_id}, {teacher_id}, {start_hour}, {end_hour}, {frequency}")
        postgres_conn.commit()
        logger.info("Class instances inserted successfully.")
    except Exception as err:
        logger.error(f"Error inserting class instances: {err}")
        postgres_conn.rollback()
