Einfaches Remote-Display für openDTU-on-Battery ohne MQTT.

Sicherlich kann man es auch auf einem ESP32 installieren, aber dazu fehlen mir die Kentnisse. 
Daher alles in herkömmlicher weise in Linus/Armbian. Lauffähig ist das Script unter LiNUX/Python und wurde auf einem OrangePiZero eingesetzt. 
Es wird automatisch beim Start geladen. (service enable start service pp.)

Das Display benötigt nur WLAN und kann überall im Netz/Haus installiert werden.
Es zeigt die wichtigsten Infos der DTU an und dient zur Überwachung des Systems

Die drei LEDs dienen der schnellen Anzeige der wichtigsten Parameter :

Gelbe LED = Sonnenenergie wird produziert.
Grüne LED = Strom wird eingespeist.
Rote LED  = Strom wird kostenpflichtig aus dem Netz bezogen.

Anstelle der LED können auch Relais angeschlossen werden. Die Anzahl der Ausgänge ist hier auf drei beschränkt. Könnte aber jederzeit erweitert werden.
Später sollen damit auch bestimmte Verbraucher angesteuert werden.

Im Hintergrund läuft nebenbei noch mein Homeassistent.
