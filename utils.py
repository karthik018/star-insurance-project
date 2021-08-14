from db_connection import get_db_connection


def store_new_policy(request_data, filename):
    db_conn = get_db_connection()
    db_cur = db_conn.cursor()
    display = int(request_data.get('display'))
    sql = "INSERT INTO Policies (PolicyName, PolicyContent, PolicyImg, Display) VALUES (%s, %s, %s, %s);"
    val = (request_data.get('policy_name'), request_data.get('policy_content'), filename, bool(display))
    db_cur.execute(sql, val)
    db_conn.commit()


def get_policies_data():
    db_conn = get_db_connection()
    db_cur = db_conn.cursor()
    sql = "SELECT PolicyName, PolicyContent, PolicyImg FROM Policies WHERE Display=TRUE"
    db_cur.execute(sql)
    rows = db_cur.fetchall()
    policies_data = [list(row) for row in rows]
    return policies_data


def get_policy_wise_content():
    db_conn = get_db_connection()
    db_cur = db_conn.cursor()
    sql = "SELECT PolicyName, PolicyContent FROM Policies"
    db_cur.execute(sql)
    rows = db_cur.fetchall()
    policy_wise_content = {row[0]: row[1] for row in rows}
    return policy_wise_content


def update_policy(request_data, filename):
    db_conn = get_db_connection()
    db_cur = db_conn.cursor()
    policy_name, policy_content, display = request_data.get('policy_name'), request_data.get('policy_content'), \
        int(request_data.get('display'))
    if filename:
        sql = 'UPDATE Policies SET PolicyContent = %s, PolicyImg = %s, Display = %s WHERE PolicyName = %s'
        val = (policy_content, filename, display, policy_name)
    else:
        sql = 'UPDATE Policies SET PolicyContent = %s, Display = %s WHERE PolicyName = %s'
        val = (policy_content, display, policy_name)
    db_cur.execute(sql, val)
    db_conn.commit()


def delete_policy(request_data):
    db_conn = get_db_connection()
    db_cur = db_conn.cursor()
    policy_name = request_data.get('policy_name')
    sql = "DELETE FROM Policies WHERE PolicyName=%s"
    db_cur.execute(sql, (policy_name, ))
    db_conn.commit()
