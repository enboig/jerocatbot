** Bot de jeroglífics

La idea és crear bot amb paquets de "jeroglífics" fets amb emoticones. L'usuari podrà escollir el joc i anar entrant els intents.
El bot anirà llegint els missatges i si comencen per número mirarà si és la resposta correcta.
També es podrà afegir el bot a un grup i anirà controlant les punctuacions.

Ja es permet editar els jocs existents des del bot mateix, així com desgarregar-los en un document .ODS i tornar-los a pujar. Quan es puja un document, si coincideixen els noms dels jocs, s'afegiran les preguntes i respostes noves només.
(Si crees jocs nous, fes-me'ls arribar ;-) )

Per fer una prova ràpida (després de renombrar i omplir config.demo.ini):
python3 initialize.py ; python3 jerocatbot.py

Per instal·lar les dependències només has de:
pip3 install -r requirements.txt

