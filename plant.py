import pymysql

# ฟังก์ชันเชื่อมต่อฐานข้อมูล
def get_connection():
    return pymysql.connect(user='root', password='', host='localhost', database='plantdb')

# ฟังก์ชันเพื่อหาลำดับรหัสถัดไป
def get_next_id():
    cnx = get_connection()
    cur = cnx.cursor()
    cur.execute("SELECT MAX(Pid) FROM tbplant")
    result = cur.fetchone()
    cur.close()
    cnx.close()
    return result[0] + 1 if result[0] else 1

# ฟังก์ชันเพิ่มข้อมูล
def add(pname, ptype, pimage):
    cnx = get_connection()
    cur = cnx.cursor()
    cur.execute("INSERT INTO tbplant (Pname, Ptype, Pimage) VALUES (%s, %s, %s)", (pname, ptype, pimage))
    cnx.commit()
    cur.close()
    cnx.close()

# ฟังก์ชันลบข้อมูล
def dele(pid):
    cnx = get_connection()
    cur = cnx.cursor()
    cur.execute("DELETE FROM tbplant WHERE Pid = %s", (pid,))
    cnx.commit()
    cur.close()
    cnx.close()

# ฟังก์ชันแก้ไขข้อมูล
def edit(pid, pname, ptype, pimage):
    cnx = get_connection()
    cur = cnx.cursor()
    cur.execute("UPDATE tbplant SET Pname=%s, Ptype=%s, Pimage=%s WHERE Pid = %s", (pname, ptype, pimage, pid))
    cnx.commit()
    cur.close()
    cnx.close()

# ฟังก์ชันแสดงข้อมูลทั้งหมด
def ShowData():
    cnx = get_connection()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM tbplant")
    rows = cur.fetchall()
    cur.close()
    cnx.close()
    return rows

# ฟังก์ชันค้นหาข้อมูล
def search_data(search_term):
    cnx = get_connection()
    cur = cnx.cursor()
    search_term = f"%{search_term}%"  # ใช้ LIKE เพื่อค้นหาแบบ fuzzy
    query = """
        SELECT * FROM tbplant
        WHERE Pid LIKE %s OR Pname LIKE %s OR Ptype LIKE %s
    """
    cur.execute(query, (search_term, search_term, search_term))
    rows = cur.fetchall()
    cur.close()
    cnx.close()
    return rows