use std::io;
use travail_chiffrement::{caesar_cipher, homophonic_encrypt, homophonic_decrypt};

fn main() {
    // Choix du type de chiffrement
    let method_choice = loop {
        println!("Choisissez le type de chiffrement :");
        println!("1 = César");
        println!("2 = Homophonic Substitution");

        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Erreur de lecture");
        let choice = input.trim();
        if choice == "1" || choice == "2" {
            break choice.to_string();
        } else {
            println!("Choix invalide, veuillez entrer 1 ou 2 !");
        }
    };

    // Choix chiffrement ou déchiffrement
    let action_choice = loop {
        println!("Que voulez-vous faire ? (1 = Chiffrement, 2 = Déchiffrement)");
        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Erreur de lecture");
        let choice = input.trim();
        if choice == "1" || choice == "2" {
            break choice.to_string();
        } else {
            println!("Choix invalide, veuillez entrer 1 ou 2 !");
        }
    };

    // Saisie du texte
    println!("Entrez le texte :");
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Erreur de lecture");
    let input = input.trim();

    // Pour César, demander la clé
    let shift = if method_choice == "1" {
        println!("Entrez la clé de décalage (shift) :");
        let mut shift_input = String::new();
        io::stdin().read_line(&mut shift_input).expect("Erreur de lecture");
        shift_input.trim().parse::<i32>().unwrap_or(3)
    } else {
        0
    };

    // Appliquer la méthode choisie
    let result = match (method_choice.as_str(), action_choice.as_str()) {
        ("1", "1") => caesar_cipher(input, shift),   // César chiffrement
        ("1", "2") => caesar_cipher(input, -shift),  // César déchiffrement
        ("2", "1") => homophonic_encrypt(input),     // Homophonic chiffrement
        ("2", "2") => homophonic_decrypt(input),     // Homophonic déchiffrement
        _ => {
            println!("Choix invalide !");
            return;
        }
    };

    println!("Résultat : {}", result);
}
