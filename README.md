# Dungeon Crawler ⚔️

Paprastas 2D požemių tyrinėjimo žaidimas su atsitiktinai generuojamais lygiais, sukurtas naudojant **Python** ir **Pygame**. Tai objektinio orientuoto programavimo (OOP) kursinis projektas.

---

## 1. Įžanga

* **Kas yra ši programa?**
    Tai yra 2D veiksmo žaidimas, kuriame žaidėjas valdo riterį, kovojantį su požemių priešais. Žaidimo esmė – panaudoti „Dash“ mechaniką priešų naikinimui ir kilti per vis sudėtingesnius lygius.
* **Kaip paleisti programą?**
    1.  Klonuokite šią saugyklą: `git clone https://github.com/tavo_vartotojas/tavo_projektas.git`
    2.  Įsitikinkite, kad turite įdiegtą Python ir Pygame biblioteką: `pip install pygame`
    3.  Paleiskite pagrindinį failą: `python dungeon_crawler.py`
* **Kaip naudotis programa?**
    * **Judėjimas:** Rodyklių klavišai (palaiko judėjimą įstrižai).
    * **Ataka / Dash:** `Space` klavišas (reikalingas sukauptas Dash item).
    * **Restartas:** Jei pralaimite (HP = 0), spauskite `R`.

---

## 2. Žaidimo analizė 

Žaidimas sukurtas taikant **OOP principus**, užtikrinant kodo skaitomumą ir plečiamumą.

### Funkcinių reikalavimų įgyvendinimas:
* **Paveldėjimas:** Visos žaidimo klasės (`Player`, `Enemy`, `Wall`, `DashItem`) paveldi bazinę `GameObject` klasę. Tai leidžia centralizuotai valdyti objektų atvaizdavimą ir kolizijų rėmus (`rect`).
 <img width="530" height="224" alt="image" src="https://github.com/user-attachments/assets/e3944a43-5a66-401c-bb6a-b26c5a582d65" />
 
* **Inkapsuliacija:** Žaidėjo hp ir is_dashing kintamieji yra inkapsuliuoti klasės viduje. Išorinis pasaulis (žaidimo ciklas) nežino, kaip tiksliai veikia „dash“ mechanika, jis tik duoda komandą pradėti.
 <img width="367" height="235" alt="image" src="https://github.com/user-attachments/assets/93094e84-20c3-4ad0-8dfc-aafbb4a86b73" />
* **Polimorfizmas:** Šis principas leidžia naudoti tą patį metodą skirtingiems objektams. Pavyzdžiui, pagrindiniame cikle aš tiesiog kviečiu .draw(self.screen) visiems objektams iš eilės, nesvarbu, ar tai siena, ar priešas – kiekvienas objektas žino, kaip save nupiešti.
 <img width="594" height="36" alt="image" src="https://github.com/user-attachments/assets/fd7cdef6-b3bc-4605-839f-225d69d0e5fd" />
* **Abstrakcija:** Vartotojui (arba pagrindiniam žaidimo ciklui) nereikia žinoti sudėtingų detalių apie tai, kaip veikia žemėlapio generavimas ar teleportacijos logika. Viskas paslėpta po paprastais metodais, tokiais kaip manager.load_map() arba player.update().
 <img width="400" height="31" alt="image" src="https://github.com/user-attachments/assets/edfd18fb-2534-4eda-8c59-e8bc95b8b67f" />
 <img width="384" height="101" alt="image" src="https://github.com/user-attachments/assets/9b33c7af-39ad-4518-8486-1d60e64429a3" />





* **Lygio generavimas:** Žemėlapiai surenkami dinamiškai iš 4 atsitiktinių tekstinių segmentų (`seg1.txt`...`seg4.txt`). Tai sukuria unikalią patirtį kiekvieną kartą žaidžiant.
* **Sklandus judėjimas:** Įgyvendintas ašinis judėjimo tikrinimas (X ir Y ašys tikrinamos atskirai). Tai sprendžia „strigimo sienose“ problemą judant įstrižai.
* **Priešų AI:** Priešai naudoja vektorių skaičiavimą žaidėjo persekiojimui, tačiau laikosi fizikos taisyklių (atsitrenkia į sienas).



---

## 3. Rezultatai ir išvados

### Rezultatai
* **Pasiekta:** Sukurta stabili žaidimo versija su progresuojančiu sudėtingumu (didėjantis priešų skaičius).
* **Iššūkiai:** Sunkiausia buvo subalansuoti priešų greitį ir žaidėjo „Dash“ atstumą, kad žaidimas būtų reikiamo sudėtingumo.
* **Sprendimai:** Klaidų taisymo metu buvo pridėti saugikliai (try-except blokai) grafikos užkrovimui, kad programa „necrashintų“ neradus failo.

### Išvados
* Programa sėkmingai demonstruoja Python panaudojimą interaktyvių programų kūrimui.
* Šis projektas pasitarnavo kaip praktinis pavyzdys, kaip OOP principai padeda valdyti sudėtingą programos būseną (State management: Playing, Game Over).
* **Ateities perspektyvos:** Galima pridėti garsų sistemą, skirtingus ginklų tipus ir labiau pažangų AI.

---

## 4. Ištekliai

* **Variklis:** [Pygame Library](https://www.pygame.org/)
* **Grafika:** Autoriniai Pixel Art resursai ir modifikuoti laisvai prieinami sprite'ai.
* **Kūrimo įrankiai:** VS Code, Git.
