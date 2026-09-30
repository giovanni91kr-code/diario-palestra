# Diario Palestra: pubblicarla con il tuo account

Alla fine avrai:

- un indirizzo tuo (es. `diario-palestra.netlify.app`);
- registrazione e login con email e password;
- lo storico completo su telefono, PC e tablet.

Tempo: 15–20 minuti, una volta sola. Costo: zero, non serve la carta di credito.

## Cosa c'è nella cartella

| File | A cosa serve |
|---|---|
| `public/` | **L'app completa**: è la cartella da pubblicare. |
| `public/firebase-config.js` | L'unico file che devi modificare: qui incolli i codici del tuo progetto. |
| `firestore.rules` | Le regole di sicurezza del database: ognuno vede solo i propri dati. |
| `firebase.json` | Serve solo se pubblichi con Firebase Hosting (opzione B del passo 5). |

---

## Passo 1: crea il progetto Firebase

1. Vai su **console.firebase.google.com** e accedi con il tuo account Google.
2. Clicca **Crea un progetto** (o "Aggiungi progetto").
3. Come nome scrivi `diario-palestra` e vai avanti.
4. Google Analytics non serve: **disattivalo**. Poi **Crea progetto**.

## Passo 2: attiva il login con email e password

1. Nel menu a sinistra apri **Authentication** (a volte si trova dentro "Crea" / "Build") e clicca **Inizia**.
2. Nella scheda **Metodo di accesso**, scegli **Email/password**.
3. Attiva il **primo** interruttore ("Email/password") e clicca **Salva**. Il secondo, "Link via email", lascialo spento.

## Passo 3: collega l'app e copia i codici

1. Torna alla **Panoramica del progetto** e clicca l'icona **`</>`** (Web).
2. Come nome dell'app scrivi `Diario Palestra`. La casella "Firebase Hosting" lascia pure non spuntata. Clicca **Registra app**.
3. Firebase ti mostra un blocco di codice che contiene `const firebaseConfig = { apiKey: "...", ... }`.
4. Apri `public/firebase-config.js` con un editor di testo (Blocco note, TextEdit o VS Code).
5. Copia i sei valori uno per uno al posto di `INCOLLA_QUI_...`. Le virgolette devono restare. Esempio:
   ```js
   apiKey: "AIzaSyB1a2b3c4...",
   authDomain: "diario-palestra-1a2b3.firebaseapp.com",
   ```
6. Salva il file.

Se ti servono di nuovo questi codici, li trovi in ⚙ **Impostazioni progetto → Generali → Le tue app**.

## Passo 4: crea il database e proteggilo

1. Nel menu apri **Firestore Database** e clicca **Crea database**. Se ti chiede l'edizione, scegli **Standard**.
2. Come posizione scegli una sede in Europa, per esempio **eur3 (Europe)** oppure **europe-west**. Non si può cambiare dopo.
3. Scegli **Modalità di produzione** e clicca **Crea**.
4. Apri la scheda **Regole**. Cancella tutto quello che c'è e incolla il contenuto del file `firestore.rules`. Poi clicca **Pubblica**.

Queste regole fanno sì che ogni account possa leggere e scrivere **solo i propri** allenamenti.

## Passo 5: metti l'app online

### Opzione A: Netlify (consigliata, senza terminale)

1. Vai su **app.netlify.com** e crea un account gratuito (puoi entrare con Google).
2. Scegli **Add new site → Deploy manually** e **trascina la cartella `public`** nel riquadro.
3. In pochi secondi ottieni un indirizzo tipo `random-name-123.netlify.app`. Per cambiarlo vai in **Site configuration → Change site name** e scrivi per esempio `diario-palestra-gio`.
4. **Importante:** torna su Firebase e apri **Authentication → Impostazioni → Domini autorizzati → Aggiungi dominio**. Scrivi il tuo indirizzo Netlify senza `https://` (es. `diario-palestra-gio.netlify.app`) e salva.

Per pubblicare un aggiornamento: su Netlify, nella scheda **Deploys**, trascina di nuovo la cartella `public`.

### Opzione B: Firebase Hosting (con il terminale)

Serve Node.js installato sul computer. Dal terminale, dentro questa cartella:
```bash
npm install -g firebase-tools
firebase login
firebase use --add        # scegli il progetto diario-palestra
firebase deploy
```
Ottieni l'indirizzo `https://<progetto>.web.app`. Il dominio viene autorizzato da solo e il comando pubblica anche le regole del database.

## Passo 6: installala sul telefono

1. Apri il tuo indirizzo dal telefono e tocca **Registrati** (email e password di almeno 6 caratteri).
2. Aggiungi l'app alla schermata Home:
   - **iPhone:** in Safari tocca **Condividi → Aggiungi alla schermata Home**.
   - **Android:** in Chrome tocca **⋮ → Installa app** (oppure "Aggiungi a schermata Home").
3. D'ora in poi si apre a schermo intero come un'app normale e funziona anche senza campo in palestra. Il salvataggio online parte appena torna la rete.

Sul PC o su un altro telefono basta aprire lo stesso indirizzo e fare **Accedi** con la stessa email e password: ritrovi tutto lo storico.

## Passo 7: porta i dati che hai già (facoltativo)

1. Nella versione su Claude apri **Dati → Backup JSON** e salva il file.
2. Nella nuova app apri **Dati → Importa backup** e scegli quel file.

Arrivano allenamenti, schede e libreria esercizi, senza doppioni.

---

## Domande frequenti

**Dove sono i miei dati?**
Nel database Firestore del tuo progetto, dentro `users/<tuo id>/data`. Ogni allenamento è un documento separato. Li puoi vedere anche dalla console Firebase, nella sezione Firestore Database. Una copia resta anche sul telefono, così l'app funziona offline.

**Tra un anno trovo ancora tutto?**
Sì. Firestore non cancella nulla e non va in pausa se non lo usi. Per stare doppiamente tranquillo, una volta ogni tanto fai **Dati → Backup JSON** o **Esporta CSV**.

**La `apiKey` nel file è un segreto?**
No. Le chiavi web di Firebase sono pubbliche per come è fatto Firebase. A proteggere i dati sono le regole del passo 4 e il login.

**Ho dimenticato la password.**
Nella schermata di accesso tocca **Password dimenticata?**. L'email arriva da `noreply@<progetto>.firebaseapp.com`: controlla anche lo spam.

**Ho pubblicato una modifica ma il telefono mostra ancora la versione vecchia.**
Chiudi l'app e riaprila (a volte servono due aperture). Se hai modificato `sw.js`, aumenta il numero in `CACHE = 'diario-palestra-v1'`.

## Se qualcosa non va

| Messaggio | Soluzione |
|---|---|
| "Manca la configurazione" | Rivedi il passo 3: i valori in `firebase-config.js` devono essere quelli del tuo progetto, tra virgolette. |
| "Questo indirizzo non è autorizzato" | Passo 5A, punto 4: aggiungi il tuo dominio Netlify nei Domini autorizzati. |
| "Login con email non attivo" | Passo 2: attiva Email/password. |
| In alto resta "Offline" anche con la rete | Controlla di aver creato il database e pubblicato le regole (passo 4). |
