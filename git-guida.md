# Guida Git

Comandi essenziali per lavorare con Git e GitHub.

## Stato del repository

```bash
git status                # mostra file modificati, aggiunti, non tracciati
git log --oneline -10     # ultimi 10 commit
git diff                  # differenze nei file modificati
git diff --staged         # differenze nei file pronti per il commit
```

## Aggiornare da GitHub

```bash
git pull origin main      # scarica e applica le modifiche remote
```

Se hai modifiche locali da preservare:
```bash
git stash                 # mette da parte le modifiche locali
git pull origin main
git stash pop             # riapplica le modifiche locali
```

## Allineare forzatamente con GitHub

Sovrascrive tutte le modifiche locali:
```bash
git fetch origin
git reset --hard origin/main
```

Per rimuovere anche i file non tracciati:
```bash
git clean -fd             # -f = force, -d = directories
git clean -fdn            # anteprima (dry-run), mostra cosa verrebbe eliminato
```

## Salvare modifiche (commit)

```bash
git add nomefile.py       # aggiunge un file specifico
git add .                 # aggiunge tutti i file modificati
git commit -m "Descrizione delle modifiche"
```

## Inviare a GitHub

```bash
git push origin main
```

## Annullare modifiche locali

```bash
git checkout -- nomefile.py      # annulla modifiche a un file
git restore nomefile.py          # equivalente (Git 2.23+)
git reset HEAD nomefile.py       # rimuove file dalla staging area
```

## Branch (rami)

```bash
git branch                        # elenca branch locali
git branch nome-branch            # crea nuovo branch
git checkout nome-branch          # passa a un branch
git checkout -b nome-branch       # crea e passa a nuovo branch
git merge nome-branch             # unisce branch nel corrente
git branch -d nome-branch         # elimina branch locale
```

## Cronologia e differenze

```bash
git log --oneline --graph         # cronologia grafica
git show abc1234                  # dettagli di un commit specifico
git diff main origin/main         # differenze tra locale e remoto
```

## Configurazione

```bash
git config --global user.name "Nome Cognome"
git config --global user.email "email@esempio.it"
git remote -v                     # mostra repository remoti collegati
```
