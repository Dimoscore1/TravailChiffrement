use std::io;
use travail_chiffrement::{
    caesar_cipher,
    caesar_then_homophonic_encrypt,
    homophonic_then_caesar_decrypt,
    vigenere_encrypt,
    vigenere_decrypt,
    remove_accents,
};

fn main() {
    println!("Choisissez le type de chiffrement :");
    println!("1 = César");
    println!("2 = Homophonic + César");
    println!("3 = Vigenère");

    let mut choice = String::new();
    io::stdin().read_line(&mut choice).expect("Erreur de lecture");
    let choice = choice.trim();

    println!("Que voulez-vous faire ? (1 = Chiffrement, 2 = Déchiffrement)");
    let mut action = String::new();
    io::stdin().read_line(&mut action).expect("Erreur de lecture");
    let action = action.trim();

    println!("Entrez le texte :");
    let mut text = String::new();
    io::stdin().read_line(&mut text).expect("Erreur de lecture");
    let mut text = text.trim().to_string();

    // On normalise les lettres
    text = remove_accents(&text);

    let result = match choice {
        "1" => {
            println!("Entrez la clé de décalage (shift) :");
            let mut shift_input = String::new();
            io::stdin().read_line(&mut shift_input).expect("Erreur de lecture");
            let shift: i32 = shift_input.trim().parse().unwrap_or(3);

            if action == "1" {
                caesar_cipher(&text, shift)
            } else {
                caesar_cipher(&text, -shift)
            }
        }
        "2" => {
            println!("Entrez la clé de décalage  :");
            let mut shift_input = String::new();
            io::stdin().read_line(&mut shift_input).expect("Erreur de lecture");
            let shift: i32 = shift_input.trim().parse().unwrap_or(3);

            if action == "1" {
                caesar_then_homophonic_encrypt(&text, shift)
            } else {
                homophonic_then_caesar_decrypt(&text, shift)
            }
        }
        "3" => {
            println!("Entrez le mot-clé (lettres uniquement) :");
            let mut key = String::new();
            io::stdin().read_line(&mut key).expect("Erreur de lecture");
            let key = key.trim();

            if action == "1" {
                vigenere_encrypt(&text, key)
            } else {
                vigenere_decrypt(&text, key)
            }
        }
        _ => {
            println!("Choix invalide !");
            return;
        }
    };

    println!("Résultat : {}", result);
}