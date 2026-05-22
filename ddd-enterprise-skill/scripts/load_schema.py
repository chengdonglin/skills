import sys
import json
import pymysql


MYSQL_CONFIG = {
    "host": "192.168.31.91",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "charset": "utf8mb4"
}


def load_schema(database):
    conn = pymysql.connect(
        **MYSQL_CONFIG,
        database=database
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
    SELECT
        TABLE_NAME,
        TABLE_COMMENT
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA=%s
    """, (database,))
    tables = cursor.fetchall()

    result = {}

    for table in tables:
        name = table["TABLE_NAME"]

        cursor.execute("""
        SELECT
            COLUMN_NAME,
            DATA_TYPE,
            COLUMN_KEY,
            IS_NULLABLE,
            COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA=%s
        AND TABLE_NAME=%s
        ORDER BY ORDINAL_POSITION
        """, (database, name))

        columns = cursor.fetchall()

        cursor.execute("""
        SELECT
            INDEX_NAME,
            COLUMN_NAME
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA=%s
        AND TABLE_NAME=%s
        """, (database, name))
        indexes = cursor.fetchall()
        cursor.execute("""
        SELECT
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA=%s
        AND TABLE_NAME=%s
        AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (database, name))

        fks = cursor.fetchall()

        result[name] = {
            "comment": table["TABLE_COMMENT"],
            "columns": columns,
            "indexes": indexes,
            "foreign_keys": fks
        }
    conn.close()
    with open("schema.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("usage: python load_schema.py <database_name>")

    load_schema(sys.argv[1])