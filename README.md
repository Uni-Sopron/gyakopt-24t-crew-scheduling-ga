
# Genetikai Algoritmus Munkabeosztáshoz

## Bevezető

Ez a projekt egy genetikai algoritmust használ a munkabeosztás optimalizálására egy 5 napos heti beosztára. 
A feladat célja, hogy biztosítsuk, hogy az elvárt létszám minden nap és minden műszakban teljesüljön, 
figyelembe véve a munkások szabadnap igényeit. 
A genetikai algoritmus segítségével próbáljuk megtalálni a legjobb beosztást, amely a lehető legjobban megfelel ezeknek a kritériumoknak.

## Kód Értelmezése

A program az alábbi lépéseket hajtja végre:

1. **Paraméterek és beállítások**:
   - Megadjuk a munkások számát, a napok és műszakok számát, valamint az elvárt létszámot minden műszakra.
   - Beállítjuk a munkások szabadnap igényeit.
   - Meghatározzuk a genetikai algoritmus paramétereit, mint a populáció mérete, a generációk száma, a mutációs és crossover arány.

2. **Genetikai Algoritmus**:
   - **Populáció létrehozása**: Véletlenszerűen létrehoz egy kezdeti populációt, ahol minden egyed egy lehetséges munkabeosztást reprezentál.
   - **Fitness értékelés**: Minden egyedre kiszámítja a fitness értéket, amely azt méri, hogy mennyire felel meg az adott beosztás az elvárt létszámnak és a munkások szabadnap igényeinek.
   - **Szelekció, Crossover és Mutáció**: A legjobb egyedek kiválasztása után crossover és mutáció segítségével új generációkat hozunk létre, remélve, hogy javítjuk a megoldások minőségét.
   - **Optimalizáció**: A folyamatot addig ismételjük, amíg el nem érjük az optimális megoldást vagy a megadott generációk számát.

3. **Eredmények Vizualizálása**:
   - A program végén egy 2D-s diagramot generálok, amely ábrázolja a generációk során elért legjobb és minimális fitness értékeket. Az optimális megoldás zöld nyíllal van kiemelve, hogy jól látható legyen.

## Eredmények Értelmezése

Az algoritmus futtatása során a cél az, hogy az optimális megoldást a lehető leghamarabb megtaláljuk, miközben a minimális fitness értékek javulnak és a legjobb fitness értékek közelítenek a maximális fitness értékhez.

A program futtatása után a konzolon megjelennek a legjobb megoldás részletei.

Az eredmények diagramja vizuálisan mutatja a genetikai algoritmus teljesítményét az optimalizáció során. A következők figyelhetők meg:

- **Legjobb Fitness Értékek (Kék vonal)**: Az egyes generációk során elért legjobb megoldások fitness értékeit mutatja.
- **Minimális Fitness Értékek (Narancssárga vonal)**: Az egyes generációk legrosszabb megoldásainak fitness értékeit ábrázolja.
- **Maximális Fitness Vonal (Piros szaggatott vonal)**: Ez a vonal az elméletileg elérhető legjobb fitness értéket jelzi.
- **Optimális Megoldás (Zöld nyíl)**: A zöld nyíl kiemeli azt a generációt, amelyben az algoritmus megtalálta az optimális megoldást. Ez a megoldás teljesíti az összes elvárt létszámot és figyelembe veszi a szabadnap igényeket is.


## Zárszó

Ez a program egy egyszerű, de hatékony példája annak, hogyan használhatók a genetikai algoritmusok összetett optimalizálási problémák megoldására. 

# EREDMÉNY:

## Legjobb megoldás megtalálva:

### Nap 1:
- Műszak 1: `[6 0]`
- Műszak 2: `[4 3]`
- Műszak 3: `[6 0]`

### Nap 2:
- Műszak 1: `[1 6]`
- Műszak 2: `[4 2]`
- Műszak 3: `[5 3]`

### Nap 3:
- Műszak 1: `[4 0]`
- Műszak 2: `[3 2]`
- Műszak 3: `[0 2]`

### Nap 4:
- Műszak 1: `[0 6]`
- Műszak 2: `[3 4]`
- Műszak 3: `[1 0]`

### Nap 5:
- Műszak 1: `[2 5]`
- Műszak 2: `[0 4]`
- Műszak 3: `[4 5]`

## Diagramm

![Eredmény Diagram](https://github.com/Uni-Sopron/gyakopt-24t-crew-scheduling-ga/blob/b8b820b3383fce9740cea1e50ec85a059addd905/eredm%C3%A9ny%20diagram.png)
