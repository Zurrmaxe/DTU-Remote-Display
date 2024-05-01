Einfaches Remote-Display für OpenDTU-on-Battery ohne MQTT. 
Es ist noch in der Entwicklung. Einiges muss noch optimiert und angepasst werden.
Es soll nur eine Anregung sein, was alles möglich ist. 
Kein fertiges Projekt.

Für die Installation auf einem OrangePiZero sind entsprechende Grundkenntisse zwingend erforderlich.
Je nach verwendetem Image sind noch diverse Librarys (Python,I2C,OLED-Treiber pp.) zu installieren,

Als Grundlage dient folgender Guthub :

https://github.com/Selbstbau-PV/Selbstbau-PV-Hoymiles-Nulleinspeisung-mit-OpenDTU-und-Shelly3EM/tree/main

Dieses Skript ist ebenso ein Fork von: https://gitlab.com/p3605/hoymiles-tarnkappe

Dieser Github wurde um ein Display und die Leuchtdioden ergänzt und an die örtlichen Gegebenheiten angepasst.

Sicherlich kann man es auch auf einem ESP32 installieren, aber dazu fehlen mir die Kenntnisse. 
Daher hier alles in herkömmlicher Weise für Linus/Armbian. 
Lauffähig ist das Script unter LiNUX/Python und wurde auf einem OrangePiZero eingesetzt. 
Es wird automatisch beim Start geladen, wenn es als service gestartet wird. (service enable start service pp.)

Das Display benötigt einen Internetzugang und kann überall im Netz/Haus installiert werden.
Es zeigt die wichtigsten Infos der DTU an und dient zur Überwachung des Systems.
Der Internetzugang bzw. WLAN wird über den OrangePiZero eingerichtet und bereitgestellt. 
Nicht über dieses Script !

Die drei LEDs dienen der schnellen Anzeige der wichtigsten Parameter :

Gelbe LED = Sonnenenergie wird produziert.
Grüne LED = Strom wird eingespeist.
Rote LED  = Strom wird kostenpflichtig aus dem Netz bezogen.

Anstelle der LED können auch Relais angeschlossen werden. Die Anzahl der Ausgänge ist hier auf drei beschränkt. Könnte aber jederzeit erweitert werden.
Später sollen mit dem Script auch bestimmte Verbraucher über Relais/Schütze angesteuert werden.

Im Hintergrund läuft bei mir zusätzlich noch andere Anwendungen u.a. noch mein Homeassistent.

Alles natürlich ohne Garantie, Gewährleistung und Haftung. 
