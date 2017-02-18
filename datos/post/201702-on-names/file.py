import json
import sqlite3

hombres = json.loads(open('hombres.json','r').read())["nombres"]
mujeres = json.loads(open('mujeres.json','r').read())["nombres"]

conn = sqlite3.connect('nombres.db')
conn.execute("CREATE TABLE nombres (nombre text, sexo text, cantidad int)")
for h in hombres:
  conn.execute("INSERT INTO nombres VALUES (?,?,?)", (h, "hombre" , int(hombres[h]['n'])))
conn.commit()
for m in mujeres:
  conn.execute("INSERT INTO nombres VALUES (?,?,?)", (m, "mujer" , int(mujeres[m]['n'])))
conn.commit()
conn.close()
