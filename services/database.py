import sqlite3 as sql


def create_user(id, api_id, api_hash, phone, phone_hash):
    users = sql.connect(r'services/madness.db')
    cursor = users.cursor()
    try:
        cursor.execute('INSERT INTO user VALUES(?, ?, ?, ?, ?)',
                    (str(id), api_id, api_hash, phone, phone_hash))
        result = 'Done!'
    except Exception as e:
        result = e
        print('except block', e)
    finally:
        users.commit()
        users.close()
    return result


def select_user(id):
    users = sql.connect(r'services/madness.db')
    cursor = users.cursor()
    try:
        result = cursor.execute('SELECT id, api_hash, api_id FROM user WHERE id = ?',
                    (str(id),)).fetchall()
    except Exception as e:
        result = e
    finally:
        users.commit()
        users.close()
    return result


def delete_user(id):
    users = sql.connect(r'services/madness.db')
    cursor = users.cursor()
    try:
        result = cursor.execute('DELETE FROM user WHERE id = ?',
                    (str(id),))
        result = 'Successfully deleted'
    except Exception as e:
        result = e
    finally:
        users.commit()
        users.close()
    return result