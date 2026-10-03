# Diario Palestra

Web app mobile-first per registrare gli allenamenti A / B / C e progredire nel tempo.

## File

| File | A cosa serve |
|---|---|
| `app.html` | Il codice sorgente dell'app (HTML + CSS + JavaScript in un unico file). È la versione pubblicata su Claude. |
| `index.html` | Versione autonoma, generata da `app.html`: si apre in qualsiasi browser o si mette online gratis (Netlify Drop, GitHub Pages). |
| `build.py` | Rigenera `index.html` dopo aver modificato `app.html` (`python3 build.py`). |
| `firebase/` | **Versione autonoma con account** (email e password, storico su tutti i dispositivi). Istruzioni in `firebase/GUIDA.md`. |
| `build_firebase.py` | Rigenera `firebase/public/index.html` da `app.html` dopo una modifica. |

## Come si usa (in palestra)

1. **Allena** → tocca Giorno A, B o C, oppure **Allenamento libero** (parti senza scheda e aggiungi gli esercizi dal menu mentre ti alleni). La scheda "Prossima" è evidenziata in blu (segue l'ordine A → B → C).
2. Ogni esercizio mostra **Ultima volta: 40 kg × 10, 10, 9** e i campi sono **già compilati** con quei valori.
3. Per ogni serie: correggi con **−/+** (o tocca il numero e scrivi), poi tocca **✓**. Il peso sale e scende di **0,5 kg** (si cambia per esercizio in Schede).
   - Il numero della serie si colora: **verde** = meglio dell'ultima volta, **grigio** = pari, **rosso** = peggio.
   - Se cambi il peso della serie 1, le serie successive si aggiornano da sole.
4. Se l'ultima volta hai chiuso il range di ripetizioni su tutte le serie, compare **"sali di peso +0,5 kg"**: un tocco e il peso aumenta su tutte le serie.
5. **Cambi idea durante la seduta?** Ogni esercizio ha due pulsanti:
   - **⇄ Sostituisci** apre la libreria divisa per parte del corpo (si apre già sul gruppo giusto, con ricerca). Serie e range restano quelli della scheda, i pesi si precompilano con l'ultima volta di quell'esercizio. La scheda base non cambia.
   - **Salta**: l'esercizio si chiude e non finisce nel registro (tocca **Ripristina** se ci ripensi).
   - **+ Esercizio extra** in fondo aggiunge un esercizio preso dalla libreria solo per oggi.
6. **Chiudi e salva** in basso → l'allenamento finisce nel **Registro**, con riepilogo di durata, volume, esercizi migliorati e record personali.

Extra durante l'allenamento: **± Serie**, **Nota** rapida (la rivedi la volta dopo), **Storico** dell'esercizio, schermo che resta acceso.
Se chiudi l'app a metà allenamento, lo ritrovi in home con **Riprendi**.

## Le altre sezioni

- **Registro** → *Allenamenti* (per data, con ▲ migliorati / ▼ peggiorati) oppure *Esercizi* (ultima volta, miglior serie, andamento, grafico della forza stimata).
- **Schede** → scegli gli esercizi da un menu a tendina diviso per parte del corpo; modifica nome scheda, serie, range ripetizioni, salto di peso, note/alternative; riordina con ↑ ↓. Si salva da solo. In fondo c'è la **Libreria esercizi** (circa 80 già pronti, compresa la categoria **Cardio**: il tapis roulant registra durata, velocità e inclinazione; cyclette, ellittica ecc. durata e livello): puoi aggiungerne o toglierne.
- **Dati** → stato del salvataggio, esporta **CSV** (Excel, una riga per serie), **backup JSON**, importa backup, ripristina schede di esempio.

## Dove finiscono i dati

- **Versione su Claude (link dell'artifact):** ogni modifica viene scritta subito sul telefono e poi nel tuo account Claude (spazio privato, visibile solo a te). Se in palestra non c'è campo non perdi nulla: l'app mette in coda e invia appena torna la rete. Stessi dati su telefono e PC.
- **Versione autonoma (`index.html`):** i dati restano nel browser del dispositivo. Fai un **Backup JSON** ogni tanto (sezione Dati).

## Come confronta le prestazioni

- Stesso peso → contano le ripetizioni.
- Più peso con ripetizioni uguali o maggiori → meglio (e viceversa).
- Casi misti (più peso ma meno reps) → confronta la forza stimata con la formula di Epley, peso × (1 + reps/30).

Tutto qui: nessuna "intelligenza" nascosta.

## Modificare il codice

`app.html` è diviso in sezioni commentate: 1 Utilità · 2 Schede di esempio · 3 Archivio · 4 Logica progressione · 5 Viste · 6 Azioni · 7 Timer · 8 Avvio.
I colori sono in cima al CSS (`:root`), le schede di esempio nella funzione `defaultPlans()`.
Nessun framework, nessuna installazione: HTML/CSS/JS puri.

## Perché questa struttura

- **Un solo file, niente backend da gestire:** si apre e basta, e resta facile da modificare.
- **Prima il telefono, poi il cloud:** il salvataggio locale è istantaneo e funziona offline; il cloud serve per non perdere niente e per usarlo su più dispositivi.
- **Precompilazione dall'ultima sessione:** in palestra di solito tocchi solo ✓, e intervieni con +/− quando migliori. Sono i tocchi minimi possibili.
- **Doppia progressione:** prima aumenti le ripetizioni dentro il range, poi il peso. È il metodo più semplice e collaudato per l'ipertrofia, e l'app lo segnala da sola.

## Aggiornamenti automatici (GitHub + Netlify)

- Codice: archivio privato GitHub `giovanni91kr-code/diario-palestra` (branch `main`).
- Sito: `https://diario-palestra-gio.netlify.app`, collegato all'archivio. Ogni modifica caricata su `main` viene pubblicata da sola in circa un minuto (impostazioni in `netlify.toml`: pubblica la cartella `firebase/public`, nessuna build).
- Dopo una modifica a `app.html`: `python3 build.py && python3 build_firebase.py`, poi commit e push.
- Il numero di versione (`APP_VERSION` in `app.html`) compare in fondo alla sezione **Dati**: serve a verificare che il telefono abbia la versione nuova.
- Dati: sempre nel progetto Firebase `diario-palestra-60f90` (Firestore). Gli aggiornamenti del sito non li toccano.
