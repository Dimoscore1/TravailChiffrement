# TravailChiffrement

Il s'agit d'un projet en Rust pour chiffrer et déchiffrer des textes avec deux méthodes :

1. **César** : un chiffrement par décalage simple.  
2. **Homophonic Substitution** : un chiffrement avec substitution de symboles réversible.

Le programme est interactif et demande à l’utilisateur de choisir le type de chiffrement, l’action (chiffrement ou déchiffrement), et la clé si nécessaire.

---

## Prérequis

- [Rust](https://www.rust-lang.org/tools/install) qui doit être installé sur la machine
- Github pour cloner le projet

---

## Installation

1. Cloner le projet :

```bash
git clone https://github.com/Dimoscore1/TravailChiffrement.git
cd TravailChiffrement

Après cela lancer : 
cargo run
Cela vous proposera 2 type de chiffrement 
Puis choisissez entre 1 et 2 pour le type de chiffrement
Puis 1 et 2 pour chiffrer ou déchiffrer
Entrer le mot a chiffrer ou à déchiffrer puis la clé de chiffrement
Test
Le projet contient des tests pour :
César (chiffrement et déchiffrement)
Homophonic Substitution (réversible)
cargo test



