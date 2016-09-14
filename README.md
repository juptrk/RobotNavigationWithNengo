# Robot Navigation mit Hilfe von Nengo

Um das Programm auszuführen, müssen Python 3, Nengo und Morse installiert werden.

Wenn Python 3 noch nicht installiert ist macht es hier Sinn, direkt Anaconda zu installieren.
Dies wird für Nengo enpfohlen und wird ebenfalls unter unten stehendem Link erklärt.

Um Nengo unter Ubuntu zu installieren folgen Sie den Schritten auf dieser Internetseite:

https://pythonhosted.org/nengo/getting_started.html#installation


Um Morse unter Ubuntu zu installieren muss lediglich folgender Befehl in die Konsole kopiert und Enter gedrückt werden:

sudo apt-get install morse-simulator


Anschließend kann mit

morse create my_first_sim
morse run my_first_sim

eine erste Simulation erstellt werden.


Um die zu diesem Programm passende Simulation zu starten sollte es genügen, den folgenden Befehl im Programmordner auszuführen:

morse run simulation

Falls dies nicht genügt, ist es auch möglich, eine neue Simulation zu erstellen, die Umgebung corridor.blend zu den
Umgebungen der neuen Simulation zu kopieren und die default.py der neuen Simulation durch die alte zu ersetzen.


Wenn die Simulation initialisiert ist, dann wird das Programm aus dem den Code beiinhaltenden Ordner mit

python3 main.py

gestartet.

Um anstelle des des Neuronenmodells den tatsächlichen Dynamic Window Approach zu verwenden müssen die Zeilen

#model = dwa.DWA()      in main.py
#self.model.move()      in robot.py

einkommentiert und die Zeilen

model = model.Model()   in main.py
self.model.step()       in robot.py

auskommentiert werde.

Viel Erfolg mit dieser Simulation!