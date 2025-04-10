import mariadb
import sys

class kundenbestellung():
    def __init__(self, anrede, name, vorname, bestelldatum, artikelname):
        self.anrede = anrede
        self.name = name
        self.vorname = vorname
        self.bestelldatum = bestelldatum
        self.artikel = artikelname

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

inp_y = int(input("Bitte den Jahr eingeben: "))
inp_m = int(input("Bitte den Monat eingeben: "))
inp_d = int(input("Bitte den Day eingeben: "))

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

for i in kundenbestell_list:
    print(i.anrede, i.name, i.vorname, i.bestelldatum, i.artikel)