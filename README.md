# Dungeon Crawler ⚔️

Paprastas 2D požemių tyrinėjimo žaidimas su atsitiktinai generuojamais lygiais, sukurtas naudojant **Python** ir **Pygame**. Tai objektinio orientuoto programavimo (OOP) kursinis projektas.

---

## 1. Introduction

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

## 2. Body/Analysis 

Žaidimas sukurtas taikant **OOP principus**, užtikrinant kodo skaitomumą ir plečiamumą.

### Funkcinių reikalavimų įgyvendinimas:
* **Paveldėjimas (Inheritance):** Visos žaidimo klasės (`Player`, `Enemy`, `Wall`, `DashItem`) paveldi bazinę `GameObject` klasę. Tai leidžia centralizuotai valdyti objektų atvaizdavimą ir kolizijų rėmus (`rect`).
* **Lygio generavimas:** Žemėlapiai surenkami dinamiškai iš 4 atsitiktinių tekstinių segmentų (`seg1.txt`...`seg4.txt`). Tai sukuria unikalią patirtį kiekvieną kartą žaidžiant.
* **Sklandus judėjimas:** Įgyvendintas ašinis judėjimo tikrinimas (X ir Y ašys tikrinamos atskirai). Tai sprendžia „strigimo sienose“ problemą judant įstrižai.
* **Priešų AI:** Priešai naudoja vektorių skaičiavimą žaidėjo persekiojimui, tačiau laikosi fizikos taisyklių (atsitrenkia į sienas).



---

## 3. Results and Summary (Rezultatai ir Išvados)

### Results (Rezultatai)
* **Pasiekta:** Sukurta stabili žaidimo versija su progresuojančiu sudėtingumu (didėjantis priešų skaičius).
* **Iššūkiai:** Sunkiausia buvo subalansuoti priešų greitį ir žaidėjo „Dash“ atstumą, kad žaidimas būtų reikiamo sudėtingumo.
* **Sprendimai:** Klaidų taisymo metu buvo pridėti saugikliai (try-except blokai) grafikos užkrovimui, kad programa „necrashintų“ neradus failo.

### Conclusions (Išvados)
* Programa sėkmingai demonstruoja Python panaudojimą interaktyvių programų kūrimui.
* Šis projektas pasitarnavo kaip praktinis pavyzdys, kaip OOP principai padeda valdyti sudėtingą programos būseną (State management: Playing, Game Over).
* **Ateities perspektyvos:** Galima pridėti garsų sistemą, skirtingus ginklų tipus ir labiau pažangų AI.

---

## 4. Resources (Ištekliai)

* **Variklis:** [Pygame Library](https://www.pygame.org/)
* **Grafika:** Autoriniai Pixel Art resursai ir modifikuoti laisvai prieinami sprite'ai.
* **Kūrimo įrankiai:** VS Code, Git.
