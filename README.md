# Untis 2.0

> Dies ist unser jüngstes Projekt (außer wir haben ein neues). Es heißt Untis 2.0 und der Name sagt eigentlich das meiste. Das Ziel von mir und meinem Geschäftspartner ist es eine Webanwendung und eine App Version von Untis zu kreieren, die für uns in der Oberstufe besser ist. Uns nervt zum Beispiel, dass für jede Stunde alle Kurse angezeigt werden und nicht nur die, die wichtig für einen sind. Und wenn man genervt ist, dann ist das nicht gesund und deswegen basteln wir ein verbessertes Untis.
<br>

# Wie funktioniert WebUntis 2.0?
> Wenn man zunächst aufruft WebUntis 2.0 stehen zwei Funktionen zur Verfügung. Man wird zunächst von der [Homepage](#homepage) begrüßt, die in unter dem Icon  <img src="assets/logo.png" alt="🕒" width="30" /> zu finden ist.
> <br>
> Desweiteren kann unter dem Plus-Zeichen ein [neues Profil](#profil-erstellen) erstellt werden: <img src="assets/plus-sign.png" alt="➕" width="30" />.
> Wird ein Profil erstellt, so ist es bei den [erstellten Profile](#existierendes-profil) zu finden, welche den ersten Buchstaben des Namens des Profils anzeigen: <img src="assets/profile-display-icon.png" alt="👤" width="30" /> und ebenso an der linken Navigationsleiste auszuwählen sind.
> ## Homepage
> ![Homepage](assets/homepage.png)
> ## Profil erstellen
> ![Profil erstellen](assets/create-profile.png)
> ## existierendes Profil
> ![existierendes Profil](assets/existing-profile.png)

# Technische Details
> ## WebUntis 2.0
> WebUntis 2.0 ist eine Dynamische Website, die mit HTML, CSS und Flask erstellt wurde. Die Daten, also gespeichtere Profile und alte Stundenpläne werden in Form von JSON Dateien gespeichert. Durch den Flask Server kann die Website aufgerufen werden und die Daten werden geladen. Daher könnte der Server theoretisch auf jedem Gerät laufen, auf dem Python und die jeweiligen Pakete installiert sind. Bis jetzt ist die Applikation jedoch nur auf Linux getestet worden. Optimierungen für andere Betriebssysteme sind auf jeden fall noch notwendig.