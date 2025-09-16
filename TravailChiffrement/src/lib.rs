use std::collections::HashMap;

/// Chiffrement César
pub fn caesar_cipher(text: &str, shift: i32) -> String {
    text.chars()
        .map(|c| {
            if c.is_ascii_lowercase() {
                let base = b'a' as i32;
                let idx = c as i32 - base;
                let new_idx = (idx + shift).rem_euclid(26);
                (base + new_idx) as u8 as char
            } else if c.is_ascii_uppercase() {
                let base = b'A' as i32;
                let idx = c as i32 - base;
                let new_idx = (idx + shift).rem_euclid(26);
                (base + new_idx) as u8 as char
            } else {
                c
            }
        })
        .collect()
}

/// Table fixe pour Homophonic Substitution (uniquement majuscules)
fn homophonic_table() -> HashMap<char, &'static str> {
    let mut table = HashMap::new();
    table.insert('A', "@");
    table.insert('B', "8");
    table.insert('C', "(");
    table.insert('D', "Ð");
    table.insert('E', "€");
    table.insert('F', "ƒ");
    table.insert('G', "6");
    table.insert('H', "#");
    table.insert('I', "!");
    table.insert('J', "¿");
    table.insert('K', "κ");
    table.insert('L', "£");
    table.insert('M', "Ü");
    table.insert('N', "ñ");
    table.insert('O', "0");
    table.insert('P', "¶");
    table.insert('Q', "φ");
    table.insert('R', "®");
    table.insert('S', "$");
    table.insert('T', "†");
    table.insert('U', "µ");
    table.insert('V', "√");
    table.insert('W', "ω");
    table.insert('X', "×");
    table.insert('Y', "¥");
    table.insert('Z', "ζ");
    table
}

/// Chiffrement Homophonic (réversible)
pub fn homophonic_encrypt(text: &str) -> String {
    let table = homophonic_table();
    text.to_uppercase()
        .chars()
        .map(|c| {
            if let Some(&symbol) = table.get(&c) {
                symbol.to_string()
            } else {
                c.to_string()
            }
        })
        .collect()
}

/// Déchiffrement Homophonic (réversible)
pub fn homophonic_decrypt(text: &str) -> String {
    let table = homophonic_table();
    let inverse_table: HashMap<_, _> = table.into_iter().map(|(k, v)| (v, k)).collect();
    let mut result = String::new();
    let mut i = 0;

    while i < text.len() {
        let mut matched = false;

        for (&symbol, &letter) in &inverse_table {
            if text[i..].starts_with(symbol) {
                result.push(letter);
                i += symbol.len();
                matched = true;
                break;
            }
        }

        if !matched {
            result.push(text.chars().nth(i).unwrap());
            i += 1;
        }
    }

    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_caesar() {
        let text = "Bonjour";
        let key = 3;
        let encrypted = caesar_cipher(text, key);
        let decrypted = caesar_cipher(&encrypted, -key);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_homophonic() {
        let text = "Bonjour";
        let encrypted = homophonic_encrypt(text);
        let decrypted = homophonic_decrypt(&encrypted);
        assert_eq!(decrypted, text.to_uppercase());
    }
}
