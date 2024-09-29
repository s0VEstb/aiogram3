CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS telegram_users (
ID integer primary key,
TELEGRAM_ID INTEGER,
USERNAME CHAR(50),
FIRST_NAME CHAR(50),
LAST_NAME CHAR(50),
UNIQUE (TELEGRAM_ID)
)"""


INSERT_USER_QUERY = """
INSERT INTO telegram_users VALUES (?,?,?,?,?)
"""


SELECT_ALL_USERS_QUERY = """
SELECT FIRST_NAME FROM telegram_users
"""