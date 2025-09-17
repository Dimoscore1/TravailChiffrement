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

/// Table pour Homophonic Substitution (que les majuscules)
fn homophonic_table() -> HashMap<char, &'static str> {
    let mut table = HashMap::new();
    table.insert('A', "F");
    table.insert('B', "8");
    table.insert('C', "E");
    table.insert('D', "l");
    table.insert('E', "€");
    table.insert('F', "J");
    table.insert('G', "6");
    table.insert('H', "#");
    table.insert('I', "!");
    table.insert('J', "¿");
    table.insert('K', "/");
    table.insert('L', "£");
    table.insert('M', "Ü");
    table.insert('N', "ñ");
    table.insert('O', "K");
    table.insert('P', "¶");
    table.insert('Q', "φ");
    table.insert('R', "®");
    table.insert('S', "D");
    table.insert('T', "U");
    table.insert('U', "µ");
    table.insert('V', "√");
    table.insert('W', "ω");
    table.insert('X', "×");
    table.insert('Y', "M");
    table.insert('Z', "ζ");
    table
}

/// Homophonic puis César 
pub fn caesar_then_homophonic_encrypt(text: &str, shift: i32) -> String {
    let caesar_text = caesar_cipher(text, shift);
    let table = homophonic_table();
    caesar_text
        .to_uppercase()
        .chars()
        .map(|c| table.get(&c).map_or(c.to_string(), |s| s.to_string()))
        .collect()
}

/// Déchiffrement homophonic puis César
pub fn homophonic_then_caesar_decrypt(text: &str, shift: i32) -> String {
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

    // On applique le décalage inverse
    caesar_cipher(&result, -shift)
}

/// Vigenère cryptage
pub fn vigenere_encrypt(text: &str, key: &str) -> String {
    let key = key.to_uppercase();
    let key_bytes = key.as_bytes();
    let mut key_index = 0;

    text.chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let shift = key_bytes[key_index % key_bytes.len()] - b'A';
                key_index += 1;
                (((c as u8 - base + shift) % 26) + base) as char
            } else {
                c
            }
        })
        .collect()
}

/// Vigenère decrypt
pub fn vigenere_decrypt(text: &str, key: &str) -> String {
    let key = key.to_uppercase();
    let key_bytes = key.as_bytes();
    let mut key_index = 0;

    text.chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let shift = key_bytes[key_index % key_bytes.len()] - b'A';
                key_index += 1;
                (((26 + c as u8 - base - shift) % 26) + base) as char
            } else {
                c
            }
        })
        .collect()
}

/// Normalisation des lettres accentuées
pub fn remove_accents(text: &str) -> String {
    text.chars()
        .map(|c| match c {
            'à' | 'á' | 'â' | 'ã' | 'ä' | 'å' => 'a',
            'ç' => 'c',
            'è' | 'é' | 'ê' | 'ë' => 'e',
            'ì' | 'í' | 'î' | 'ï' => 'i',
            'ñ' => 'n',
            'ò' | 'ó' | 'ô' | 'õ' | 'ö' => 'o',
            'ù' | 'ú' | 'û' | 'ü' => 'u',
            'ý' | 'ÿ' => 'y',
            'À' | 'Á' | 'Â' | 'Ã' | 'Ä' | 'Å' => 'A',
            'Ç' => 'C',
            'È' | 'É' | 'Ê' | 'Ë' => 'E',
            'Ì' | 'Í' | 'Î' | 'Ï' => 'I',
            'Ò' | 'Ó' | 'Ô' | 'Õ' | 'Ö' => 'O',
            'Ù' | 'Ú' | 'Û' | 'Ü' => 'U',
            'Ý' => 'Y',
            _ => c,
        })
        .collect()
}
#[cfg(test)]
mod tests {
    use super::*;

    // Test de César
    #[test]
    fn test_caesar_lowercase() {
        let text = "Chateau";
        let shift = 3;
        let encrypted = caesar_cipher(text, shift);
        let decrypted = caesar_cipher(&encrypted, -shift);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_caesar_uppercase() {
        let text = "DOUVE";
        let shift = 5;
        let encrypted = caesar_cipher(text, shift);
        let decrypted = caesar_cipher(&encrypted, -shift);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_caesar_mixed() {
        let text = "Sieur, Gauvain! 1er du nom";
        let shift = 4;
        let encrypted = caesar_cipher(text, shift);
        let decrypted = caesar_cipher(&encrypted, -shift);
        assert_eq!(decrypted, text);
    }

    // ----------------- Tests Homophonic + César -----------------
    #[test]
    fn test_homophonic_caesar_uppercase() {
        let text = "PRINCESSE";
        let shift = 2;
        let encrypted = caesar_then_homophonic_encrypt(text, shift);
        let decrypted = homophonic_then_caesar_decrypt(&encrypted, shift);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_homophonic_caesar_lowercase() {
        let text = "reine";
        let shift = 3;
        let encrypted = caesar_then_homophonic_encrypt(text, shift);
        let decrypted = homophonic_then_caesar_decrypt(&encrypted, shift);
        assert_eq!(decrypted, text.to_uppercase());
    }

    #[test]
    fn test_homophonic_caesar_mixed() {
        let text = "Pontlevis";
        let shift = 1;
        let encrypted = caesar_then_homophonic_encrypt(text, shift);
        let decrypted = homophonic_then_caesar_decrypt(&encrypted, shift);
        assert_eq!(decrypted, text.to_uppercase());
    }

    // Tests de Vigenère 
    #[test]
    fn test_vigenere_uppercase() {
        let text = "REMPART";
        let key = "Chateau";
        let encrypted = vigenere_encrypt(text, key);
        let decrypted = vigenere_decrypt(&encrypted, key);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_vigenere_lowercase() {
        let text = "epee";
        let key = "Manche";
        let encrypted = vigenere_encrypt(text, key);
        let decrypted = vigenere_decrypt(&encrypted, key);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_vigenere_mixed_text() {
        let text = "Pour la paix";
        let key = "Accord";
        let encrypted = vigenere_encrypt(text, key);
        let decrypted = vigenere_decrypt(&encrypted, key);
        assert_eq!(decrypted, text);
    }

    #[test]
    fn test_vigenere_with_accents() {
        let text = "Je te declare la Guerre!";
        let normalized = remove_accents(text);
        let key = "REGICIDE";
        let encrypted = vigenere_encrypt(&normalized, key);
        let decrypted = vigenere_decrypt(&encrypted, key);
        assert_eq!(decrypted, normalized);
    }

    #[test]
    fn test_vigenere_long_key() {
        let text = "Anticonstitutionnellement";
        let key = "Dinosaure";
        let encrypted = vigenere_encrypt(text, key);
        let decrypted = vigenere_decrypt(&encrypted, key);
        assert_eq!(decrypted, text);
    }
}

