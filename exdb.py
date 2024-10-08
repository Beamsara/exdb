import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from plant import add, dele, edit, ShowData, get_next_id, search_data

# ฟังก์ชันแสดงข้อมูลใน Treeview
def show_data():
    rows = ShowData()
    update_tree(rows)

# ฟังก์ชันค้นหา
def on_search():
    search_term = search_entry.get()  # ดึงค่าจากช่องค้นหา
    if search_term:
        # เรียกฟังก์ชัน search_data เพื่อค้นหาข้อมูลที่ตรงกับคำค้นหา
        rows = search_data(search_term)
        update_tree(rows)  # อัปเดตผลลัพธ์ลงใน tree_widget
    else:
        # ถ้าไม่ใส่คำค้นหา ให้แสดงข้อมูลทั้งหมด
        show_data()


# ฟังก์ชันอัปเดตข้อมูลใน Treeview
def update_tree(rows):
    for i in tree_widget.get_children():
        tree_widget.delete(i)  # ลบข้อมูลเดิมทั้งหมด
    for row in rows:
        tree_widget.insert('', 'end', values=row)  # เพิ่มข้อมูลใหม่ที่ได้จากการค้นหา

# ฟังก์ชันเลือกไฟล์ภาพและบันทึก path ไว้ในตัวแปร
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        image_label.config(text=file_path)
        global pimage
        pimage = file_path  # เก็บ path ของภาพในตัวแปร

# ฟังก์ชันเมื่อคลิกที่แถวใน tree_widget
def on_tree_select(event):
    selected_item = tree_widget.selection()
    if selected_item:
        # ดึงค่าจากแถวที่เลือก
        values = tree_widget.item(selected_item, 'values')
        
        # แสดงค่าลงในฟอร์ม
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])  # ชื่อ

        type_combobox.set(values[2])  # ประเภท

        # สมมติว่า path ของภาพถูกเก็บในฐานข้อมูลและเป็นค่าใน values[3]
        global pimage
        pimage = values[3]
        image_button.config(text=pimage)  # แสดง path ของภาพ
        # อัปเดตรหัสใน code_value (values[0] คือรหัส)
        code_value.config(text=values[0])  # แสดงรหัสของข้อมูลที่เลือก

# ฟังก์ชันเพิ่มต้นไม้
def on_add():
    pname = name_entry.get()
    ptype = type_combobox.get()
    add(pname, ptype, pimage)  # ใช้ pimage ที่ได้จากการเลือกภาพ
    show_data()
    messagebox.showinfo("Success", "ข้อมูลต้นไม้ถูกเพิ่มเรียบร้อยแล้ว!")
    clear_form()

# ฟังก์ชันลบต้นไม้
def on_delete():
    selected_item = tree_widget.selection()
    if selected_item:
        pid = tree_widget.item(selected_item)['values'][0]
        dele(pid)
        show_data()
        messagebox.showinfo("Success", "ข้อมูลต้นไม้ถูกลบเรียบร้อยแล้ว!")
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกข้อมูลที่จะลบ")

# ฟังก์ชันแก้ไขต้นไม้
def on_edit():
    selected_item = tree_widget.selection()
    if selected_item:
        pid = tree_widget.item(selected_item)['values'][0]
        pname = name_entry.get()
        ptype = type_combobox.get()
        edit(pid, pname, ptype, pimage)
        show_data()
        messagebox.showinfo("Success", "ข้อมูลต้นไม้ถูกแก้ไขเรียบร้อยแล้ว!")
    else:
        messagebox.showwarning("Warning", "กรุณาเลือกข้อมูลที่จะแก้ไข")

# ฟังก์ชันเคลียร์ฟอร์ม
def clear_form():
    name_entry.delete(0, tk.END)
    type_combobox.set("เลือกประเภท")
    image_label.config(text="เลือกภาพ")

# ฟังก์ชันปรับขนาดหน้าต่างให้อยู่ตรงกลาง
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width // 2 - size[0] // 2
    y = screen_height // 2 - size[1] // 2
    window.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Tree Information Manager")
root.geometry("850x650")
style = ttk.Style()

# ตั้งค่าธีมของ ttk widgets
style.theme_use('clam')

# ปรับการปรับขนาดของหน้าต่าง
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# สร้างเฟรมหลักสำหรับ layout
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

# ปรับ column และ row ของ main_frame ให้ขยายได้
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)

# เฟรมส่วนการค้นหา
search_frame = ttk.Frame(main_frame, padding="5", relief="solid")
search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
search_frame.grid_columnconfigure(1, weight=1)

# ป้ายและช่องค้นหา
search_label = ttk.Label(search_frame, text="ค้นหา")
search_label.grid(row=0, column=0, padx=5, pady=5)

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

search_button = ttk.Button(search_frame, text="ค้นหา")
search_button.config(command=on_search)
search_button.grid(row=0, column=2, padx=5, pady=5)

# เฟรมส่วนแสดงข้อมูล
info_frame = ttk.Frame(main_frame, padding="5", relief="solid")
info_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
info_frame.grid_columnconfigure(1, weight=1)

# รหัสต้นไม้
next_id = get_next_id()
code_label = ttk.Label(info_frame, text="รหัส:")
code_label.grid(row=0, column=0, padx=5, pady=5)
code_value = ttk.Label(info_frame, text=f"{next_id}")  # รหัสของต้นไม้
code_value.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# ชื่อต้นไม้
name_label = ttk.Label(info_frame, text="ชื่อต้นไม้:")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_entry = ttk.Entry(info_frame, width=30)
name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# ประเภทต้นไม้ (Dropdown)
type_label = ttk.Label(info_frame, text="ประเภท:")
type_label.grid(row=2, column=0, padx=5, pady=5)

# สร้าง dropdown list สำหรับประเภทต้นไม้
type_values = ["ไม้ดอก", "ไม้ประดับ", "ไม้ยืนต้น"]
type_combobox = ttk.Combobox(info_frame, values=type_values, state="readonly")
type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
type_combobox.set("เลือกประเภท")  # ตั้งค่าตัวเลือกเริ่มต้น

# ปุ่มเลือกภาพ
image_label = ttk.Label(info_frame, text="ภาพ:")
image_label.grid(row=3, column=0, padx=5, pady=5)
image_button = ttk.Button(info_frame, text="เลือกภาพ", command=select_image)
image_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# สร้างเฟรมสำหรับปุ่มต่างๆ
button_frame = ttk.Frame(main_frame, padding="5")
button_frame.grid(row=1, column=1, sticky="n", padx=10, pady=10)

add_button = ttk.Button(button_frame, text="Add", command=on_add)
add_button.grid(row=0, column=0, padx=5, pady=5)

delete_button = ttk.Button(button_frame, text="Delete", command=on_delete)
delete_button.grid(row=1, column=0, padx=5, pady=5)

update_button = ttk.Button(button_frame, text="Update", command=on_edit)
update_button.grid(row=2, column=0, padx=5, pady=5)

# เฟรมแสดง Tree widget
tree_frame = ttk.Frame(main_frame, padding="5", relief="solid")
tree_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

tree_widget = ttk.Treeview(tree_frame, columns=("Id", "Name", "Type", "Image"), show="headings", height=10)
tree_widget.heading("Id", text="รหัส")
tree_widget.heading("Name", text="ชื่อ")
tree_widget.heading("Type", text="ประเภท")
tree_widget.heading("Image", text="ภาพ")
tree_widget.grid(row=0, column=0, sticky="nsew")

# การจัดการ column weight ใน tree frame
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

# ผูก event เมื่อมีการเลือกแถวใน Treeview
tree_widget.bind("<<TreeviewSelect>>", on_tree_select)

# ฟังก์ชันเริ่มต้นแสดงข้อมูล
show_data()

# ปรับขนาดหน้าต่างให้อยู่ตรงกลางเมื่อเริ่มต้นโปรแกรม
center_window(root)

# เริ่มต้น main loop ของโปรแกรม
root.mainloop()
