# Journal — Sécurité, test d'injection et erreurs rencontrées

## 1. Test d'injection SQL (`' OR '1'='1`)
- **Appel testé :** `lister_societes(conn, secteur="' OR '1'='1")`
- **Résultat observé :** `0` ligne renvoyée (`[]`).
- **Explication :** Toutes les requêtes SQL de `depot.py` utilisent des paramètres positionnels `%s` via PyMySQL ; la chaîne saisie est traitée comme une valeur littérale et jamais interprétée comme du code SQL.

## 2. Compte applicatif dédié (moindre privilège)
- L'application utilise l'utilisateur `app_financier` (`@127.0.0.1` et `@localhost`) disposant uniquement de `SELECT, INSERT, UPDATE, DELETE` sur `client_financier.*`, sans privilège administrateur `root`.
- Les identifiants réels restent dans `.env` (ignoré par Git) ; `.env.example` ne contient aucune valeur sensible.

## 3. Erreurs rencontrées et solutions
1. **Commande `nano.env` / `nano. env` introuvable :** un espace est requis entre `nano` et le nom de fichier (`nano .env`).
2. **Déplacement dans `~/.venv` :** la commande `cd .venv` a changé le répertoire courant ; retour au dossier projet avec `cd ~/acces_donnees_financier`.
3. **Mot de passe par défaut sur `app_financier` :** résolu avec `ALTER USER ... IDENTIFIED BY '...'` et `FLUSH PRIVILEGES`, puis mise à jour de `DB_PASSWORD` dans `.env`.
4. **Exécution de `recharger_jeu_test.py` avant sa création :** `No such file or directory` ; résolu en créant `recharger_jeu_test.py` avant de l'exécuter et de l'ajouter à Git.
