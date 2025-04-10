import tkinter
from tkinter import ttk
import mariadb
import sys 

def ins(rows):
    for item in treeview.get_children():
        treeview.delete(item)

    for col_name in cols:
        treeview.heading(col_name, text=col_name)

    for value_tuple in rows:
        row = []
        row.append(value_tuple.name)
        row.append(value_tuple.vorname)
        row.append(value_tuple.anrede)
        row.append(value_tuple.bestelldatum)
        row.append(value_tuple.artikelname)
        treeview.insert('', tkinter.END, values=row)

def search():
    inp_y = int(year_entry.get())
    inp_m = int(month_entry.get())
    inp_d = int(day_entry.get())

    cur.execute(f"""SELECT kunden.Name, kunden.Vorname, anrede.Anrede, bestellungen.Bestelldatum, artikel.Artikelname
        FROM (((kunden JOIN bestellungen 
        ON kunden.IDKUNDE = bestellungen.ID_KUNDE) 
        JOIN zuordnung_bestellungen_artikel 
        ON bestellungen.ID_Bestellung = zuordnung_bestellungen_artikel.ID_Bestellung) 
        JOIN artikel 
        ON zuordnung_bestellungen_artikel.ID_ARTIKEL = artikel.artikelnummer) 
        JOIN anrede 
        ON kunden.Anrede = anrede.`ID_Anrede`
        WHERE Bestelldatum >= '{inp_y}-{inp_m}-{inp_d}'""")
    
    kundenbestell_list = []

    for i, j, k, l, m in cur:
        kundenbestell_list.append(kundenbestellung(i, j, k, l, m))

    ins(kundenbestell_list)
    
class kundenbestellung():
    def __init__(self, anrede, name, vorname, bestelldatum, artikelname):
        self.anrede = anrede
        self.name = name
        self.vorname = vorname
        self.bestelldatum = bestelldatum
        self.artikelname = artikelname

try:
    conn = mariadb.connect(
        user="Geister_Eule",
        password="Jd787811?",
        host="localhost",
        port=3306,
        database="schlumpfshop3"
    )
except mariadb.Error as e:
    print(f"Error {e}")
    sys.exit(1)

cur = conn.cursor()

root = tkinter.Tk()

cols = ("Name", "Vorname", "Anrede", "Bestelldatum", "Artikelname")

style = ttk.Style(root)
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Search")
widgets_frame.grid(row=0, column=0, padx=10, pady=10)

year_entry = ttk.Entry(widgets_frame)
year_entry.insert(0, "Jahr")
year_entry.bind("<FocusIn>", lambda e: year_entry.delete('0', 'end'))
year_entry.grid(row=1, column=0, padx=5, pady=(0,5), sticky="ew")

month_entry = ttk.Entry(widgets_frame)
month_entry.insert(0, "Monat")
month_entry.bind("<FocusIn>", lambda e: month_entry.delete('0', 'end'))
month_entry.grid(row=2, column=0, padx=5, pady=(0,5), sticky="ew")

day_entry = ttk.Entry(widgets_frame)
day_entry.insert(0, "Tag")
day_entry.bind("<FocusIn>", lambda e: day_entry.delete('0', 'end'))
day_entry.grid(row=3, column=0, padx=5, pady=(0,5), sticky="ew")

button_insert = ttk.Button(widgets_frame, text="Insert", command=search)
button_insert.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10, padx=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)
treeview.column("Name", width=100)
treeview.column("Vorname", width=100)
treeview.column("Anrede", width=100)
treeview.column("Bestelldatum", width=200)
treeview.column("Artikelname", width=100)
treeview.pack()
treeScroll.config(command=treeview.yview)

root.mainloop()