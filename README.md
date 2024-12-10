# Automatisation d'un système de gestion d'inventaire
Cours de Développement Informatique II - V. Van den Schrieck, X. Dubruille -Décembre 2024
## Documentation
- [Fonctionnalités](https://github.com/Sleeeee/t201-script/wiki/Fonctionnalit%C3%A9s)
- Rapport sur l'[utilisation de l'IA](https://github.com/Sleeeee/t201-script/wiki/Utilisation-de-l'IA)
## Utilisation
### Arguments
Le script s'exécute via la ligne de commande avec l'interpréteur Python : `python src/main.py`. Voici un bref aperçu des arguments qui peuvent lui être passés :
- `generate` : génère des fichiers de données dans `~/.t201-script/`.
  * `-f` ou `--files` : nombre de fichiers à générer. 10 par défaut.
  * `-r` ou `--rows` : nombre de lignes de données par fichier. 200 par défaut.
- `fetch` : récupère le contenu des fichiers dans `~/.t201-script/`.
  * `-f` ou `--filter` : n'affiche que les lignes correspondant à l'expression logique entrée. Une expression logique prend la forme de `column "operator" value`, par exemple `Company "==" GitHub`. Argument cumulable.
  * `-s` ou `--sort` : trie les résultats selon le nom de colonne entré.
  * `-r` ou `--reverse` : si le tri est activé, trie de manière décroissante.
  * `-c` ou `--column` : n'affiche que les colonnes spécifiées (ou toutes si aucune indiquée). Argument cumulable.

Lors d'un `fetch`, le programme demande à l'utilisateur s'il souhaite exporter les résultats au format JSON, avec ou sans les statistiques générées. Pour confirmer, il suffit d'entrer `y` ou `n` dans le terminal.

### Exemples
Je veux générer 5 fichiers longs de 300 lignes chacun :
```
[t201-script] python src/main.py generate -f 5 -r 300
```

Je veux récupérer toutes les données des produits dont la valeur de la colonne `Stock` est supérieure à 100 : 
```
[t201-script] python src/main.py fetch -f Stock ">" 100
```
Je veux récupérer uniquement les données de prix unitaire des produits des entreprises dont le nom se situe avant la lettre F dans l'alphabet. Ces données doivent être triées par leur prix en ordre décroissant : 
```
[t201-script] python src/main.py fetch -c "Unit Price" -f Company "<" F -s "Unit Price" -r
```
