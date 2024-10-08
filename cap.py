import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pymysql
import os

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Plant Management")
root.geometry("720x720")

# การเชื่อมต่อฐานข้อมูล
cnx = pymysql.connect(user='root', password='', host='localhost', database='plantdb')
cur = cnx.cursor()

# ฟังก์ชันในการค้นหารหัสถัดไป
def get_next_id():
    cur.execute("SELECT MAX(Pid) FROM tbplant")
    result = cur.fetchone()
    return result[0] + 1 if result[0] else 1

# ฟังก์ชันสำหรับการเพิ่มข้อมูล
def add():
    try:
        pname = entry_name.get()
        ptype = dropdown_type.get()
        img_path = entry_image.get()
        count = cur.execute("INSERT INTO tbplant (Pname, Ptype, Pimage) VALUES (%s, %s, %s)", (pname, ptype, img_path))
        cnx.commit()
        messagebox.showinfo("Success", "Data added successfully")
        show_data()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ฟังก์ชันสำหรับการลบข้อมูล
def delete():
    try:
        selected_item = tree.selection()[0]
        plant_id = tree.item(selected_item)['values'][0]
        cur.execute("DELETE FROM tbplant WHERE Pid = %s", (plant_id,))
        cnx.commit()
        messagebox.showinfo("Success", "Data deleted successfully")
        show_data()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ฟังก์ชันสำหรับการแก้ไขข้อมูล
def update():
    try:
        selected_item = tree.selection()[0]
        plant_id = tree.item(selected_item)['values'][0]
        pname = entry_name.get()
        ptype = dropdown_type.get()
        img_path = entry_image.get()
        cur.execute("UPDATE tbplant SET Pname=%s, Ptype=%s, Pimage=%s WHERE Pid = %s", (pname, ptype, img_path, plant_id))
        cnx.commit()
        messagebox.showinfo("Success", "Data updated successfully")
        show_data()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ฟังก์ชันสำหรับการค้นหา
def find():
    search_text = entry_search.get()
    query = "SELECT * FROM tbplant WHERE Pname LIKE %s"
    cur.execute(query, ('%' + search_text + '%',))
    rows = cur.fetchall()
    update_tree(rows)

# ฟังก์ชันในการเลือกไฟล์ภาพ
def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    entry_image.delete(0, tk.END)
    entry_image.insert(0, file_path)

# ฟังก์ชันในการแสดงข้อมูลใน Treeview
def show_data():
    cur.execute("SELECT * FROM tbplant")
    rows = cur.fetchall()
    update_tree(rows)

# ฟังก์ชันในการอัปเดต Treeview
def update_tree(rows):
    for i in tree.get_children():
        tree.delete(i)
    for row in rows:
        tree.insert('', 'end', values=row)
    
# ส่วน UI
frame_search = tk.Frame(root, pady=10, padx=10)
frame_search.pack()

label_search = tk.Label(frame_search, text="ค้นหา")
label_search.pack(side=tk.LEFT)

entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT)

btn_search = tk.Button(frame_search, text="ค้นหา", command=find)
btn_search.pack(side=tk.LEFT)

frame_form = tk.Frame(root, pady=10, padx=10)
frame_form.pack()

# รหัสถัดไปจากฐานข้อมูล
next_id = get_next_id()
label_id = tk.Label(frame_form, text=f"รหัส: {next_id}")
label_id.grid(row=0, column=0)

label_name = tk.Label(frame_form, text="ชื่อต้นไม้:")
label_name.grid(row=1, column=0)

entry_name = tk.Entry(frame_form)
entry_name.grid(row=1, column=1)

label_type = tk.Label(frame_form, text="ประเภท:")
label_type.grid(row=2, column=0)

# สร้าง dropdown สำหรับประเภท
dropdown_type = ttk.Combobox(frame_form, values=["ไม้ดอก", "ไม้ประดับ", "ไม้ยืนต้น"])
dropdown_type.grid(row=2, column=1)
dropdown_type.current(0)  # ตั้งค่าเริ่มต้นให้เป็น "ไม้ดอก"

label_image = tk.Label(frame_form, text="ภาพ")
label_image.grid(row=3, column=0)

entry_image = tk.Entry(frame_form)
entry_image.grid(row=3, column=1)

btn_image = tk.Button(frame_form, text="เลือกภาพ", command=choose_image)
btn_image.grid(row=3, column=2)

frame_buttons = tk.Frame(root)
frame_buttons.pack()

btn_add = tk.Button(frame_buttons, text="Add", command=add)
btn_add.grid(row=0, column=0)

btn_delete = tk.Button(frame_buttons, text="Delete", command=delete)
btn_delete.grid(row=0, column=1)

btn_update = tk.Button(frame_buttons, text="Update", command=update)
btn_update.grid(row=0, column=2)

# Treeview สำหรับแสดงข้อมูล
tree = ttk.Treeview(root, columns=('ID', 'Name', 'Type'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Type', text='Type')
tree.pack(fill=tk.BOTH, expand=True)

# แสดงข้อมูลเมื่อเริ่มต้นโปรแกรม
show_data()

root.mainloop()
