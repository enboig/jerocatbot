** Bot de jeroglífics

La idea és crear bot amb paquets de "jeroglífics" fets amb emoticones. L'usuari podrà escollir el joc i anar entrant els intents.
El bot anirà llegint els missatges i si comencen per número mirarà si és la resposta correcta.
També es podrà afegir el bot a un grup i anirà controlant les puntuacions.

També es permet editar els jocs existents des del bot mateix, així com desgarregar-los en un document .ODS i tornar-los a pujar. Quan es puja un document, si coincideixen els noms dels jocs, s'afegiran les preguntes i respostes noves només.
(Si crees jocs nous, fes-me'ls arribar ;-) )

Per instal·lar les dependències només has de:
pip3 install -r requirements.txt

*** Coses apreses:
- La primera biblioteca utilitzada per treballar amb telegram es penjava al cap d'unes quantes hores sense enviar missatges, l'he acabat substituïnt a mig projecte.
- Si la BBDD és sqlite, les repostes han de ser quasi perfectes (no és sensible a majúscules ni minúscules, però si als accents).
- Si la BBDD és mariadb, les respostes no són sensibles als accents, però alguns emojis eren equivalents, o sigui que ha calgut canviar la col·lació a binària.
- Els resultats mostraven o el "username" o el "first_name"+"last_name"; quan un usuari només tenia "first_name" fallava perquè el cognom era None.
