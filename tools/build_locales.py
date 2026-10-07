from pathlib import Path
import re, html, argparse
ROOT=Path(__file__).resolve().parents[1]
LANGS=['cs','en','de','sk','pl']
BASE=argparse.ArgumentParser()
BASE.add_argument('--base-url',default='https://wootrex.cz/')
base=BASE.parse_args().base_url.rstrip('/')+'/'
# Each row is Czech | English | German | Slovak | Polish.
rows = """
Zpětná vazba|Feedback|Feedback|Spätná väzba|Opinia
Android může požádat o povolení instalace aplikací z tohoto zdroje, protože beta je distribuována mimo Google Play.|Android may ask for permission to install apps from this source because the beta is distributed outside Google Play.|Android kann um die Erlaubnis bitten, Apps aus dieser Quelle zu installieren, da die Beta außerhalb von Google Play verteilt wird.|Android môže požiadať o povolenie inštalácie aplikácií z tohto zdroja, pretože beta je distribuovaná mimo Google Play.|Android może poprosić o zgodę na instalowanie aplikacji z tego źródła, ponieważ wersja beta jest udostępniana poza Google Play.
Menu|Menu|Menü|Menu|Menu
Přejít na obsah|Skip to content|Zum Inhalt springen|Prejsť na obsah|Przejdź do treści
WOOTREX — úvod|WOOTREX — home|WOOTREX — Startseite|WOOTREX — úvod|WOOTREX — strona główna
Otevřít navigaci|Open navigation|Navigation öffnen|Otvoriť navigáciu|Otwórz nawigację
Hlavní navigace|Main navigation|Hauptnavigation|Hlavná navigácia|Nawigacja główna
Funkce|Features|Funktionen|Funkcie|Funkcje
Progres|Progress|Fortschritt|Progres|Postępy
Kontakt|Contact|Kontakt|Kontakt|Kontakt
Chci testovat|Join the beta|Beta testen|Chcem testovať|Chcę testować
TVŮJ TRÉNINK. TVŮJ PROGRES.|YOUR TRAINING. YOUR PROGRESS.|DEIN TRAINING. DEIN FORTSCHRITT.|TVOJ TRÉNING. TVOJ PROGRES.|TWÓJ TRENING. TWOJE POSTĘPY.
Trénuj.|Train.|Trainiere.|Trénuj.|Trenuj.
Sleduj progres.|Track progress.|Verfolge deinen Fortschritt.|Sleduj progres.|Śledź postępy.
Staň se svou|Become your|Werde deine|Staň sa svojou|Stań się swoją
další verzí.|next version.|nächste Version.|ďalšou verziou.|kolejną wersją.
WOOTREX spojuje silový trénink, kardio, outdoor aktivity a sledování postavy do jednoho místa.|WOOTREX brings strength training, cardio, outdoor activities and body tracking together in one place.|WOOTREX vereint Krafttraining, Cardio, Outdoor-Aktivitäten und Körperentwicklung an einem Ort.|WOOTREX spája silový tréning, kardio, outdoor aktivity a sledovanie postavy na jednom mieste.|WOOTREX łączy trening siłowy, cardio, aktywności na świeżym powietrzu i śledzenie sylwetki w jednym miejscu.
Chci testovat WOOTREX|Test WOOTREX|WOOTREX testen|Chcem testovať WOOTREX|Chcę testować WOOTREX
Zjistit více|Learn more|Mehr erfahren|Zistiť viac|Dowiedz się więcej
ANDROID V UZAVŘENÉM TESTOVÁNÍ|ANDROID IN CLOSED TESTING|ANDROID IM GESCHLOSSENEN TEST|ANDROID V UZAVRETOM TESTOVANÍ|ZAMKNIĘTE TESTY ANDROIDA
iOS PŘIPRAVUJEME|iOS COMING NEXT|iOS IN VORBEREITUNG|iOS PRIPRAVUJEME|iOS W PRZYGOTOWANIU
EST. 2026 / BUILT FOR PROGRESS|EST. 2026 / BUILT FOR PROGRESS|SEIT 2026 / FÜR FORTSCHRITT GEMACHT|OD ROKU 2026 / PRE PROGRES|OD 2026 / DLA POSTĘPÓW
Kovové logo WX se zeleným akcentem|Metallic WX logo with a green accent|Metallisches WX-Logo mit grünem Akzent|Kovové logo WX so zeleným akcentom|Metaliczne logo WX z zielonym akcentem
Kovové logo WX|Metallic WX logo|Metallisches WX-Logo|Kovové logo WX|Metaliczne logo WX
01 / KEEP MOVING|01 / KEEP MOVING|01 / BLEIB IN BEWEGUNG|01 / ZOSTAŇ V POHYBE|01 / NIE ZATRZYMUJ SIĘ
Aktivity|Activities|Aktivitäten|Aktivity|Aktywności
SÍLA|STRENGTH|KRAFT|SILA|SIŁA
VYTRVALOST|ENDURANCE|AUSDAUER|VYTRVALOSŤ|WYTRZYMAŁOŚĆ
POHYB|MOVEMENT|BEWEGUNG|POHYB|RUCH
PROGRES|PROGRESS|FORTSCHRITT|PROGRES|POSTĘPY
01 / FUNKCE|01 / FEATURES|01 / FUNKTIONEN|01 / FUNKCIE|01 / FUNKCJE
Každý pohyb.|Every movement.|Jede Bewegung.|Každý pohyb.|Każdy ruch.
Jedno místo.|One place.|Ein Ort.|Jedno miesto.|Jedno miejsce.
Od první série po poslední kilometr.|From the first set to the last kilometre.|Vom ersten Satz bis zum letzten Kilometer.|Od prvej série po posledný kilometer.|Od pierwszej serii do ostatniego kilometra.
Všechno, co posouvá tvoji další verzi.|Everything that moves your next version forward.|Alles, was dich zu deiner nächsten Version bringt.|Všetko, čo posúva tvoju ďalšiu verziu.|Wszystko, co prowadzi do twojej kolejnej wersji.
Silový trénink|Strength training|Krafttraining|Silový tréning|Trening siłowy
Série, opakování, váhy, osobní rekordy a tréninkové plány.|Sets, reps, weights, personal records and workout plans.|Sätze, Wiederholungen, Gewichte, persönliche Rekorde und Trainingspläne.|Série, opakovania, váhy, osobné rekordy a tréningové plány.|Serie, powtórzenia, ciężary, rekordy osobiste i plany treningowe.
SÍLA & TECHNIKA|STRENGTH & TECHNIQUE|KRAFT & TECHNIK|SILA & TECHNIKA|SIŁA & TECHNIKA
Běh a chůze|Running and walking|Laufen und Gehen|Beh a chôdza|Bieganie i chodzenie
GPS záznam, vzdálenost, čas, tempo a tvoje trasa.|GPS recording, distance, time, pace and your route.|GPS-Aufzeichnung, Distanz, Zeit, Tempo und deine Route.|GPS záznam, vzdialenosť, čas, tempo a tvoja trasa.|Zapis GPS, dystans, czas, tempo i twoja trasa.
KAŽDÝ KILOMETR|EVERY KILOMETRE|JEDER KILOMETER|KAŽDÝ KILOMETER|KAŻDY KILOMETR
Kolo a kardio|Cycling and cardio|Radfahren und Cardio|Bicykel a kardio|Rower i cardio
Kardio aktivity a výkon. Měj přehled o své vytrvalosti.|Cardio activities and performance. Keep track of your endurance.|Cardio-Aktivitäten und Leistung. Behalte deine Ausdauer im Blick.|Kardio aktivity a výkon. Maj prehľad o svojej vytrvalosti.|Aktywności cardio i wyniki. Śledź swoją wytrzymałość.
Statistiky a progres|Statistics and progress|Statistiken und Fortschritt|Štatistiky a progres|Statystyki i postępy
Porovnávej období, tréninkový objem a svůj vývoj.|Compare periods, training volume and your development.|Vergleiche Zeiträume, Trainingsvolumen und deine Entwicklung.|Porovnávaj obdobia, tréningový objem a svoj vývoj.|Porównuj okresy, objętość treningową i swój rozwój.
ŠIRŠÍ PERSPEKTIVA|THE BIGGER PICTURE|DER GESAMTÜBERBLICK|ŠIRŠIA PERSPEKTÍVA|SZERSZA PERSPEKTYWA
Postava a tělesné míry|Physique and body measurements|Körper und Körpermaße|Postava a telesné miery|Sylwetka i wymiary ciała
Hmotnost, tělesné míry a dlouhodobý progres v souvislostech.|Weight, body measurements and long-term progress in context.|Gewicht, Körpermaße und langfristiger Fortschritt im Zusammenhang.|Hmotnosť, telesné miery a dlhodobý progres v súvislostiach.|Masa ciała, wymiary i długoterminowe postępy w szerszym ujęciu.
TVŮJ VÝVOJ|YOUR DEVELOPMENT|DEINE ENTWICKLUNG|TVOJ VÝVOJ|TWÓJ ROZWÓJ
Fotografie proměny|Transformation photos|Veränderungsfotos|Fotografie premeny|Zdjęcia przemiany
Vizuální progres a porovnání postavy v průběhu času.|Visual progress and physique comparison over time.|Sichtbarer Fortschritt und Körpervergleich im Zeitverlauf.|Vizuálny progres a porovnanie postavy v priebehu času.|Wizualne postępy i porównanie sylwetki na przestrzeni czasu.
VIDITELNÁ ZMĚNA|VISIBLE CHANGE|SICHTBARE VERÄNDERUNG|VIDITEĽNÁ ZMENA|WIDOCZNA ZMIANA
WOOTREX V AKCI|WOOTREX IN ACTION|WOOTREX IN AKTION|WOOTREX V AKCII|WOOTREX W AKCJI
Všechno, co potřebuješ.|Everything you need.|Alles, was du brauchst.|Všetko, čo potrebuješ.|Wszystko, czego potrzebujesz.
V jednom tréninkovém systému.|In one training system.|In einem Trainingssystem.|V jednom tréningovom systéme.|W jednym systemie treningowym.
Prohlédni si obrazovky posunutím do strany →|Swipe sideways to explore the screens →|Wische seitlich, um die Ansichten zu entdecken →|Pozri si obrazovky posunutím do strany →|Przesuń w bok, aby zobaczyć ekrany →
Skutečné obrazovky aplikace WOOTREX|Real WOOTREX app screens|Echte Ansichten der WOOTREX-App|Skutočné obrazovky aplikácie WOOTREX|Rzeczywiste ekrany aplikacji WOOTREX
WOOTREX: probíhající silový trénink, čas pauzy a zápis sérií|WOOTREX: active strength workout, rest timer and set logging|WOOTREX: laufendes Krafttraining, Pausentimer und Satzerfassung|WOOTREX: prebiehajúci silový tréning, čas prestávky a zápis sérií|WOOTREX: trening siłowy, licznik przerwy i zapis serii
WOOTREX: statistiky tréninkového objemu, sérií a osobních rekordů|WOOTREX: training volume, set and personal record statistics|WOOTREX: Statistiken zu Trainingsvolumen, Sätzen und persönlichen Rekorden|WOOTREX: štatistiky tréningového objemu, sérií a osobných rekordov|WOOTREX: statystyki objętości treningowej, serii i rekordów osobistych
WOOTREX: porovnání fotografií postavy a přehled tělesných změn|WOOTREX: physique photo comparison and body changes overview|WOOTREX: Vergleich von Körperfotos und Übersicht der Veränderungen|WOOTREX: porovnanie fotografií postavy a prehľad telesných zmien|WOOTREX: porównanie zdjęć sylwetki i przegląd zmian ciała
Trénink|Training|Training|Tréning|Trening
Statistiky|Statistics|Statistiken|Štatistiky|Statystyki
Postava|Physique|Körper|Postava|Sylwetka
02 / PROGRES|02 / PROGRESS|02 / FORTSCHRITT|02 / PROGRES|02 / POSTĘPY
Nejen pocit.|Beyond a feeling.|Mehr als ein Gefühl.|Nielen pocit.|Więcej niż odczucie.
Viditelný posun.|Visible progress.|Sichtbarer Fortschritt.|Viditeľný posun.|Widoczne postępy.
Každý trénink je dílek. WOOTREX ti pomůže vidět celý obraz.|Every workout is a piece. WOOTREX helps you see the whole picture.|Jedes Training ist ein Baustein. WOOTREX hilft dir, das Gesamtbild zu sehen.|Každý tréning je dielik. WOOTREX ti pomôže vidieť celý obraz.|Każdy trening to element układanki. WOOTREX pomaga zobaczyć całość.
Historie tréninků|Workout history|Trainingshistorie|História tréningov|Historia treningów
Osobní rekordy a tréninkový objem|Personal records and training volume|Persönliche Rekorde und Trainingsvolumen|Osobné rekordy a tréningový objem|Rekordy osobiste i objętość treningowa
GPS aktivity|GPS activities|GPS-Aktivitäten|GPS aktivity|Aktywności GPS
Hmotnost a tělesné míry|Weight and body measurements|Gewicht und Körpermaße|Hmotnosť a telesné miery|Masa i wymiary ciała
Fotografie postavy|Physique photos|Körperfotos|Fotografie postavy|Zdjęcia sylwetki
TVÁ DALŠÍ VERZE|YOUR NEXT VERSION|DEINE NÄCHSTE VERSION|TVOJA ĎALŠIA VERZIA|TWOJA KOLEJNA WERSJA
TRÉNINK|TRAINING|TRAINING|TRÉNING|TRENING
AKTIVITY|ACTIVITIES|AKTIVITÄTEN|AKTIVITY|AKTYWNOŚCI
POSTAVA|PHYSIQUE|KÖRPER|POSTAVA|SYLWETKA
Ilustrace oblastí progresu · nejde o obrazovku aplikace ani skutečná data|Illustration of progress areas · not an app screen or real data|Illustration der Fortschrittsbereiche · keine App-Ansicht oder echten Daten|Ilustrácia oblastí progresu · nejde o obrazovku aplikácie ani skutočné dáta|Ilustracja obszarów postępu · nie jest ekranem aplikacji ani rzeczywistymi danymi
03 / BUĎ U TOHO|03 / BE PART OF IT|03 / SEI DABEI|03 / BUĎ PRI TOM|03 / DOŁĄCZ
WOOTREX je nyní v uzavřeném testování pro Android a připravuje se iOS verze přes TestFlight.|WOOTREX is currently in closed testing for Android, with an iOS version via TestFlight in preparation.|WOOTREX befindet sich im geschlossenen Android-Test. Eine iOS-Version über TestFlight wird vorbereitet.|WOOTREX je teraz v uzavretom testovaní pre Android a pripravuje sa iOS verzia cez TestFlight.|WOOTREX jest obecnie w zamkniętych testach na Androidzie. Wersja iOS przez TestFlight jest w przygotowaniu.
Uzavřené testování|Closed testing|Geschlossener Test|Uzavreté testovanie|Zamknięte testy
TestFlight připravujeme|TestFlight in preparation|TestFlight in Vorbereitung|TestFlight pripravujeme|TestFlight w przygotowaniu
Chci se zapojit do testování|Join the testing programme|Am Test teilnehmen|Chcem sa zapojiť do testovania|Chcę dołączyć do testów
Napiš nám. Společně posuneme WOOTREX dál.|Write to us. Together we can move WOOTREX forward.|Schreib uns. Gemeinsam bringen wir WOOTREX weiter.|Napíš nám. Spoločne posunieme WOOTREX ďalej.|Napisz do nas. Razem rozwiniemy WOOTREX.
THE NEXT<br>VERSION IS YOU.|THE NEXT<br>VERSION IS YOU.|DU BIST DIE<br>NÄCHSTE VERSION.|ĎALŠIA VERZIA<br>SI TY.|KOLEJNA WERSJA<br>TO TY.
04 / KONTAKT|04 / CONTACT|04 / KONTAKT|04 / KONTAKT|04 / KONTAKT
Jsme na příjmu.|We're listening.|Wir sind für dich da.|Sme na príjme.|Jesteśmy do dyspozycji.
Zpětná vazba, nápad nebo zájem o betu?|Feedback, an idea or interested in the beta?|Feedback, eine Idee oder Interesse an der Beta?|Spätná väzba, nápad alebo záujem o betu?|Opinia, pomysł lub zainteresowanie betą?
Privacy Policy|Privacy Policy|Datenschutzerklärung|Ochrana súkromia|Polityka prywatności
"""
maps={l:{} for l in LANGS}
for row in rows.strip().splitlines():
 cols=row.split('|'); assert len(cols)==5,row
 for i,l in enumerate(LANGS):maps[l][cols[0]]=cols[i]
maps['cs']['Privacy Policy']='Ochrana soukromí'
maps['cs']['EST. 2026 / BUILT FOR PROGRESS']='OD ROKU 2026 / PRO PROGRES'
maps['cs']['01 / KEEP MOVING']='01 / ZŮSTAŇ V POHYBU'
maps['cs']['THE NEXT<br>VERSION IS YOU.']='DALŠÍ VERZE<br>JSI TY.'
# Translate once, longest strings first, to avoid cascading replacements.
def translate(s,l):
 keys=sorted(maps[l],key=len,reverse=True)
 return re.sub('|'.join(re.escape(k) for k in keys),lambda m:maps[l][m[0]],s)
privacy_titles={
 'cs':'Ochrana soukromí','en':'Privacy Policy','de':'Datenschutzerklärung','sk':'Ochrana súkromia','pl':'Polityka prywatności'}
descs={
 'cs':'Silový trénink, kardio, outdoor aktivity a sledování postavy na jednom místě. Zapoj se do uzavřeného testování WOOTREX.',
 'en':'Strength training, cardio, outdoor activities and body tracking in one place. Join WOOTREX closed testing.',
 'de':'Krafttraining, Cardio, Outdoor-Aktivitäten und Körperentwicklung an einem Ort. Nimm am geschlossenen WOOTREX-Test teil.',
 'sk':'Silový tréning, kardio, outdoor aktivity a sledovanie postavy na jednom mieste. Zapoj sa do uzavretého testovania WOOTREX.',
 'pl':'Trening siłowy, cardio, aktywności na świeżym powietrzu i śledzenie sylwetki w jednym miejscu. Dołącz do zamkniętych testów WOOTREX.'}
policy={}
source=(ROOT/'tools/templates/privacy.html').read_text(encoding='utf-8-sig')
for l,section_id in [('cs','cesky'),('en','english')]:
 policy[l]=re.search(r'<section id="'+section_id+r'".*?>(.*?)</section>',source,re.S)[1]
policy['de']="""
<h2>Datenschutzerklärung</h2><p>Diese Erklärung beschreibt den aktuellen Umgang mit Daten in der WOOTREX-App und auf ihrer Website. Bei Fragen zum Datenschutz wende dich an wootrex@seznam.cz.</p>
<h3>Trainings- und Körperdaten</h3><p>Trainingsdaten, Körpergewicht und Körpermaße werden lokal auf dem Gerät gespeichert. Vom Nutzer ausgewählte oder aufgenommene Körperfotos werden lokal verwendet und gespeichert.</p>
<h3>Standort und Geräteberechtigungen</h3><ul><li>GPS wird zur Aufzeichnung von Outdoor-Aktivitäten verwendet.</li><li>Auf Kamera und Fotobibliothek wird nur zugegriffen, wenn der Nutzer eine Funktion aufruft, die dies erfordert.</li><li>Das Mikrofon darf nur von Funktionen verwendet werden, die ausdrücklich eine Aufnahme erfordern.</li></ul><p>Du kannst Berechtigungen in den Geräteeinstellungen erteilen oder widerrufen.</p>
<h3>Kartenkacheln</h3><p>Beim Anzeigen einer Karte einer aufgezeichneten Outdoor-Route lädt die App Kartenkacheln über HTTPS von OpenStreetMap (tile.openstreetmap.org). Der Anbieter erhält deine IP-Adresse, technische Anfrageinformationen und Kennungen der angeforderten Kacheln, aus denen sich das angezeigte Gebiet ableiten lässt. Die Route wird auf dem Gerät gezeichnet; diese Funktion lädt nicht die vollständige GPS-Aufzeichnung zu OpenStreetMap hoch. Der Anbieter beschreibt die Verarbeitung der Anfragen in der <a href="https://osmfoundation.org/wiki/Privacy_Policy">Datenschutzerklärung der OpenStreetMap Foundation</a>.</p>
<h3>Aufbewahrung und Löschung lokaler Daten</h3><p>Lokale Daten dienen der Trainingshistorie, der Aktivitätsaufzeichnung und der Verfolgung der Körperentwicklung und verbleiben im App-Speicher, bis sie entfernt werden. Körpereinträge und ihre Fotos können in der App gelöscht werden. Lokaler App-Speicher kann über die Optionen des Betriebssystems zum Entfernen von App-Daten oder zur Deinstallation entfernt werden; die genauen Optionen hängen von der Plattform ab. Originale in der Fotobibliothek, exportierte oder geteilte Kopien und etwaige Systemsicherungen müssen separat verwaltet werden. WOOTREX kann Daten, die nur auf deinem Gerät gespeichert sind, nicht aus der Ferne löschen.</p>
<h3>Vom Nutzer veranlasstes Teilen</h3><p>Wenn du ein Veränderungsfoto exportierst oder teilst, wird der ausgewählte Inhalt an die von dir gewählte App oder den Empfänger übergeben. Die weitere Verarbeitung unterliegt deren Regeln.</p>
<h3>Tracking und Datenweitergabe</h3><p>WOOTREX verwendet kein Werbetracking und verkauft keine personenbezogenen Daten. Derzeit erfasst kein WOOTREX-Analysebackend Trainings-, Körper- oder Standortdaten.</p>
<h3>Feedback</h3><p>Das Feedbackformular der Website und die kommende App-Version senden Nachricht, Kategorie, optionale Kontakt-E-Mail und begrenzte technische Metadaten per HTTPS an die WOOTREX Feedback API. Der Inhalt wird zur Bearbeitung des Feedbacks in Cloudflare D1 gespeichert. Metadaten umfassen Quelle, Plattform, Sprache und in der App die verfügbare Version, Build-Nummer und aktuelle Ansicht. Trainingsdaten, Körpermaße, Fotos, GPS und Nutzerkennungen werden nicht automatisch angehängt. Cloudflare verarbeitet beim Übertragen die IP-Adresse und technische Anfrageinformationen; die IP dient der Spam-Begrenzung und wird nicht in der Feedback-Tabelle gespeichert. Gib nur Informationen an, die du senden möchtest. Die bestehende Beta 1 kann weiterhin E-Mail-Feedback anbieten; E-Mails an wootrex@seznam.cz werden von den E-Mail-Anbietern des Absenders und Empfängers verarbeitet.</p>
<h3>Diese Website</h3><p>Die WOOTREX-Website verwendet Cloudflare Web Analytics, um den Website-Traffic und die Nutzung der Seiten in aggregierter Form zu verstehen. Diese Analyse wird nicht für Werbung verwendet und verwendet keine Tracking-Cookies. WOOTREX verwendet weder Google Analytics noch Werbetracker und verkauft keine Besucherdaten.</p>
<h3>Künftige Änderungen</h3><p>Diese Erklärung kann sich ändern, wenn Konten, Cloud-Synchronisierung, Analysen oder andere Online-Dienste eingeführt werden. Die aktualisierte Fassung wird auf dieser Seite mit einem neuen Aktualisierungsdatum veröffentlicht.</p>
"""
policy['sk']="""
<h2>Zásady ochrany súkromia</h2><p>Tieto zásady opisujú súčasné spracúvanie údajov v aplikácii a na webe WOOTREX. Otázky o súkromí môžete poslať na wootrex@seznam.cz.</p>
<h3>Tréningové a telesné údaje</h3><p>Údaje o tréningoch, telesnej hmotnosti a telesných mierach sú ukladané lokálne v zariadení. Fotografie postavy, ktoré používateľ vyberie alebo vytvorí, sú používané a ukladané lokálne.</p>
<h3>Poloha a oprávnenia zariadenia</h3><ul><li>GPS sa používa na zaznamenávanie outdoor aktivít.</li><li>Kamera a knižnica fotografií sú sprístupnené iba vtedy, keď používateľ spustí funkciu, ktorá ich potrebuje.</li><li>Mikrofón môže byť používaný iba funkciou, ktorá výslovne vyžaduje nahrávanie.</li></ul><p>Oprávnenia môžete udeliť alebo odvolať v nastaveniach zariadenia.</p>
<h3>Mapové podklady</h3><p>Pri zobrazení mapy zaznamenanej outdoor trasy aplikácia načítava mapové dlaždice cez HTTPS zo služby OpenStreetMap (tile.openstreetmap.org). Poskytovateľ tak prijíma IP adresu, technické údaje požiadavky a označenia požadovaných dlaždíc, z ktorých možno odvodiť zobrazenú oblasť. Trasa sa kreslí v zariadení; táto funkcia nenahráva celý GPS záznam do OpenStreetMap. Spracúvanie požiadaviek poskytovateľom opisujú <a href="https://osmfoundation.org/wiki/Privacy_Policy">zásady súkromia OpenStreetMap Foundation</a>.</p>
<h3>Uchovávanie a odstránenie lokálnych údajov</h3><p>Lokálne údaje slúžia na históriu tréningov, záznam aktivít a sledovanie vývoja postavy a zostávajú v úložisku aplikácie, kým nie sú odstránené. Záznamy postavy a ich fotografie možno odstrániť v aplikácii. Lokálne úložisko aplikácie možno odstrániť prostredníctvom možností operačného systému na odstránenie údajov aplikácie alebo odinštalovanie; presné možnosti závisia od platformy. Originály v knižnici fotografií, exportované či zdieľané kópie a prípadné systémové zálohy je potrebné spravovať osobitne. WOOTREX nemôže vzdialene odstrániť údaje uložené iba vo vašom zariadení.</p>
<h3>Zdieľanie zvolené používateľom</h3><p>Ak použijete export alebo zdieľanie fotografie premeny, zvolený obsah sa odovzdá vami vybranej aplikácii či príjemcovi a ďalšie spracúvanie sa riadi ich pravidlami.</p>
<h3>Sledovanie a odovzdávanie údajov</h3><p>WOOTREX nepoužíva reklamné sledovanie a nepredáva osobné údaje. V súčasnosti žiadny analytický backend WOOTREX nezhromažďuje údaje o tréningoch, tele alebo polohe.</p>
<h3>Spätná väzba</h3><p>Formulár spätnej väzby na webe a v pripravovanej verzii aplikácie odosiela správu, kategóriu, prípadný kontaktný e-mail a obmedzené technické údaje cez HTTPS do WOOTREX Feedback API. Obsah bude uložený v Cloudflare D1 na vybavenie spätnej väzby. Údaje zahŕňajú zdroj, platformu, jazyk a v aplikácii dostupnú verziu, číslo zostavenia a aktuálnu obrazovku. Tréningy, telesné miery, fotografie, GPS ani identifikátory používateľa sa automaticky neprikladajú. Cloudflare počas prenosu spracúva IP adresu a technické údaje požiadavky; IP sa používa na obmedzenie spamu a neukladá sa do tabuľky feedback. Uvádzajte iba informácie, ktoré chcete odoslať. Existujúca Beta 1 môže naďalej ponúkať e-mailovú spätnú väzbu; e-maily na wootrex@seznam.cz spracúvajú poskytovatelia e-mailu odosielateľa a príjemcu.</p>
<h3>Tento web</h3><p>Web WOOTREX používa Cloudflare Web Analytics na porozumenie súhrnnej návštevnosti webu a využívania stránok. Táto analytika sa nepoužíva na reklamu a nepoužíva sledovacie cookies. WOOTREX nepoužíva Google Analytics ani reklamné sledovacie prvky a nepredáva údaje návštevníkov.</p>
<h3>Budúce zmeny</h3><p>Tieto zásady sa môžu zmeniť pri zavedení účtov, cloudovej synchronizácie, analytiky alebo ďalších online služieb. Aktualizovaná verzia bude zverejnená na tejto stránke s novým dátumom aktualizácie.</p>
"""
policy['pl']="""
<h2>Polityka prywatności</h2><p>Ta polityka opisuje obecne przetwarzanie danych w aplikacji WOOTREX i na jej stronie internetowej. Pytania dotyczące prywatności można kierować na wootrex@seznam.cz.</p>
<h3>Dane treningowe i dane dotyczące ciała</h3><p>Dane treningowe, masa ciała i wymiary ciała są przechowywane lokalnie na urządzeniu. Zdjęcia sylwetki wybrane lub wykonane przez użytkownika są wykorzystywane i przechowywane lokalnie.</p>
<h3>Lokalizacja i uprawnienia urządzenia</h3><ul><li>GPS służy do rejestrowania aktywności na świeżym powietrzu.</li><li>Aparat i biblioteka zdjęć są dostępne wyłącznie wtedy, gdy użytkownik uruchomi funkcję, która ich wymaga.</li><li>Mikrofon może być używany wyłącznie przez funkcję, która wyraźnie wymaga nagrywania.</li></ul><p>Uprawnienia można przyznawać lub cofać w ustawieniach urządzenia.</p>
<h3>Kafelki mapy</h3><p>Podczas wyświetlania mapy zarejestrowanej trasy na świeżym powietrzu aplikacja pobiera kafelki mapy przez HTTPS z OpenStreetMap (tile.openstreetmap.org). Dostawca otrzymuje adres IP, informacje techniczne żądania i identyfikatory żądanych kafelków, z których można wywnioskować wyświetlany obszar. Trasa jest rysowana na urządzeniu; ta funkcja nie przesyła całego zapisu GPS do OpenStreetMap. Sposób przetwarzania żądań przez dostawcę opisuje <a href="https://osmfoundation.org/wiki/Privacy_Policy">polityka prywatności OpenStreetMap Foundation</a>.</p>
<h3>Przechowywanie i usuwanie danych lokalnych</h3><p>Dane lokalne służą do historii treningów, rejestrowania aktywności i śledzenia zmian sylwetki i pozostają w pamięci aplikacji do momentu usunięcia. Wpisy dotyczące sylwetki i ich zdjęcia można usuwać w aplikacji. Lokalną pamięć aplikacji można usunąć za pomocą dostępnych w systemie operacyjnym opcji usuwania danych aplikacji lub odinstalowania; dokładne opcje zależą od platformy. Oryginałami w bibliotece zdjęć, wyeksportowanymi lub udostępnionymi kopiami oraz ewentualnymi kopiami zapasowymi systemu należy zarządzać oddzielnie. WOOTREX nie może zdalnie usunąć danych przechowywanych wyłącznie na urządzeniu użytkownika.</p>
<h3>Udostępnianie z inicjatywy użytkownika</h3><p>Jeśli wyeksportujesz lub udostępnisz zdjęcie przemiany, wybrana treść zostanie przekazana do wskazanej aplikacji lub odbiorcy, a dalsze przetwarzanie podlega ich zasadom.</p>
<h3>Śledzenie i przekazywanie danych</h3><p>WOOTREX nie stosuje śledzenia reklamowego i nie sprzedaje danych osobowych. Obecnie żaden backend analityczny WOOTREX nie gromadzi danych treningowych, danych dotyczących ciała ani lokalizacji.</p>
<h3>Opinie</h3><p>Formularz opinii na stronie i w nadchodzącej wersji aplikacji wysyła wiadomość, kategorię, opcjonalny e-mail kontaktowy i ograniczone metadane techniczne przez HTTPS do WOOTREX Feedback API. Treść będzie przechowywana w Cloudflare D1 w celu obsługi opinii. Metadane obejmują źródło, platformę, język oraz w aplikacji dostępną wersję, numer kompilacji i bieżący ekran. Treningi, wymiary ciała, zdjęcia, GPS i identyfikatory użytkownika nie są dołączane automatycznie. Cloudflare przetwarza podczas transmisji adres IP i techniczne dane żądania; IP służy do ograniczania spamu i nie jest zapisywany w tabeli feedback. Podawaj tylko informacje, które chcesz wysłać. Istniejąca Beta 1 może nadal oferować opinie przez e-mail; wiadomości na wootrex@seznam.cz są przetwarzane przez dostawców poczty nadawcy i odbiorcy.</p>
<h3>Ta strona internetowa</h3><p>Strona WOOTREX używa Cloudflare Web Analytics, aby zrozumieć zagregowany ruch na stronie i korzystanie z jej stron. Ta analityka nie jest używana do reklamy i nie używa śledzących plików cookie. WOOTREX nie używa Google Analytics ani trackerów reklamowych i nie sprzedaje danych odwiedzających.</p>
<h3>Przyszłe zmiany</h3><p>Ta polityka może się zmienić wraz z wprowadzeniem kont, synchronizacji w chmurze, analityki lub innych usług online. Zaktualizowana wersja zostanie opublikowana na tej stronie z nową datą aktualizacji.</p>
"""
locale={'cs':'cs_CZ','en':'en_GB','de':'de_DE','sk':'sk_SK','pl':'pl_PL'}
labels={'cs':['Jazyk','Zavřít navigaci','Zpět na web','Poslední aktualizace: 7. října 2026'],
'en':['Language','Close navigation','Back to website','Last updated: 7 October 2026'],
'de':['Sprache','Navigation schließen','Zurück zur Website','Zuletzt aktualisiert: 7. Oktober 2026'],
'sk':['Jazyk','Zavrieť navigáciu','Späť na web','Posledná aktualizácia: 7. októbra 2026'],
'pl':['Język','Zamknij nawigację','Powrót na stronę','Ostatnia aktualizacja: 7 października 2026']}
def selector(l,prefix='',privacy=False):
 dest='privacy.html' if privacy else ''
 links=[]
 for code,label in zip(LANGS,['CZ','EN','DE','SK','PL']):
  current=' aria-current="page"' if code==l else ''
  links.append(f'<a href="{prefix}{code}/{dest}" hreflang="{code}" lang="{code}" data-language="{code}"{current}>{label}</a>')
 return f'<div class="locale-selector" role="group" aria-label="{labels[l][0]}">'+'<span aria-hidden="true"> / </span>'.join(links)+'</div>'
def seo(l,privacy=False):
 suffix='privacy.html' if privacy else ''
 url=base+l+'/'+suffix
 title=privacy_titles[l]+' — WOOTREX' if privacy else 'WOOTREX — '+translate('Trénuj. Sleduj progres.',l)
 desc=(privacy_titles[l]+': WOOTREX. '+{'cs':'Lokální data, oprávnění a kontakt.','en':'Local data, permissions and contact.','de':'Lokale Daten, Berechtigungen und Kontakt.','sk':'Lokálne údaje, oprávnenia a kontakt.','pl':'Dane lokalne, uprawnienia i kontakt.'}[l]) if privacy else descs[l]
 result=f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc,quote=True)}">\n<link rel="canonical" href="{url}">\n'
 for code in LANGS:
  result+=f'<link rel="alternate" hreflang="{code}" href="{base}{code}/{suffix}">\n'
 result+=f'<link rel="alternate" hreflang="x-default" href="{base}cs/{suffix}">\n'
 for key,val in [('type','website'),('locale',locale[l]),('title',title),('description',desc),('url',url),('image',base+'assets/images/wootrex-splash-logo.png'),('image:alt',translate('Kovové logo WX',l))]:
  result+=f'<meta property="og:{key}" content="{html.escape(val,quote=True)}">\n'
 return result
template=(ROOT/'tools/templates/index.html').read_text(encoding='utf-8-sig')
for l in LANGS:
 folder=ROOT/l;folder.mkdir(exist_ok=True)
 s=translate(template,l)
 s=s.replace('<html lang="cs">',f'<html lang="{l}">')
 s=re.sub(r'<title>.*?<link rel="icon"',seo(l)+'<link rel="icon"',s,flags=re.S)
 s=s.replace('src="assets/', 'src="../assets/').replace('href="assets/', 'href="../assets/')
 s=s.replace('</nav></header>',selector(l,'../')+'</nav></header>',1)
 s=s.replace('<button class="menu-toggle"',f'<button data-open-label="{translate("Otevřít navigaci",l)}" data-close-label="{labels[l][1]}" class="menu-toggle"')
 s=s.replace('</head>','<script src="../assets/js/language.js" defer></script>\n</head>')
 (folder/'index.html').write_text(s.rstrip()+'\n',encoding='utf-8')
 title=privacy_titles[l]
 p=f'''<!doctype html>
<html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080b0a">
{seo(l,True)}
<link rel="icon" type="image/png" href="../assets/images/wootrex-splash-logo.png" sizes="1254x1254"><link rel="stylesheet" href="../assets/css/style.css"><script src="../assets/js/language.js" defer></script><script src="../assets/js/feedback.js" defer></script></head>
<body><a class="skip" href="#main">{translate('Přejít na obsah',l)}</a><header class="header privacy-header"><a class="brand" href="./"><img src="../assets/images/wootrex-splash-logo.png" width="48" height="48" alt=""><span>WOOTREX</span></a><a class="text-link" href="./">← {labels[l][2]}</a>{selector(l,'../',True)}</header>
<main class="section privacy" id="main"><p class="eyebrow">WOOTREX / {title.upper()}</p><h1>{title}</h1><p>{labels[l][3]}</p><section lang="{l}">{policy[l]}</section></main>
<footer class="footer"><div><a class="brand" href="./">WOOTREX</a><p class="slogan">YOUR NEXT VERSION</p></div><div class="footer-links"><button type="button" class="button small" data-feedback>{translate("Zpětná vazba",l)}</button><a href="./#kontakt">{translate('Kontakt',l)}</a><span>© 2026 WOOTREX</span></div></footer></body></html>
'''
 (folder/'privacy.html').write_text(p,encoding='utf-8')
# Czech root fallback: fully rendered content, browser selection only at this entry point.
root=(ROOT/'cs/index.html').read_text(encoding='utf-8').replace('../assets/','assets/').replace('href="../','href="')
root=root.replace('href="privacy.html"','href="cs/privacy.html"')
root=root.replace('<body>','<body data-language-entry="true">')
(ROOT/'index.html').write_text(root,encoding='utf-8')
# Keep the established bilingual privacy URL, with crawlable links to the five policies.
legacy=source
legacy=re.sub(r'<title>.*?<link rel="icon"',seo('cs',True)+'<link rel="icon"',legacy,flags=re.S)
legacy=legacy.replace('</head>','<script src="assets/js/language.js" defer></script></head>')
legacy=legacy.replace('</header>',selector('cs','',True)+'</header>',1).replace('class="header"','class="header privacy-header"',1)
(ROOT/'privacy.html').write_text(legacy.rstrip()+'\n',encoding='utf-8')
print('Generated 10 localized pages and two root compatibility pages.')

# Install the supplied public beacon exactly once in each published page.
BEACON = '<!-- Cloudflare Web Analytics --><script type=\'module\' src=\'https://static.cloudflareinsights.com/beacon.min.js\' data-cf-beacon=\'{"token": "a9252c3488074632afb1ec502d532257"}\'></script><!-- End Cloudflare Web Analytics -->'
for page in [ROOT/'index.html', ROOT/'privacy.html'] + [ROOT/l/name for l in LANGS for name in ['index.html','privacy.html']]:
 content=page.read_text(encoding='utf-8')
 assert 'static.cloudflareinsights.com' not in content, page
 assert content.count('</body>')==1, page
 page.write_text(content.replace('</body>', BEACON+'\n</body>'),encoding='utf-8')
