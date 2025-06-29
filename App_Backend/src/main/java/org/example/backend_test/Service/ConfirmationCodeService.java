package org.example.backend_test.Service;

import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ConfirmationCodeService {

    // Structure pour stocker code + expiration
    private static class CodeEntry {
        String code;
        LocalDateTime expiresAt;

        CodeEntry(String code, LocalDateTime expiresAt) {
            this.code = code;
            this.expiresAt = expiresAt;
        }
    }

    private final Map<String, CodeEntry> codeMap = new ConcurrentHashMap<>();

    // Générer et stocker un code temporaire (valide 5 minutes)
    public String generateAndStoreCode(String email) {
        String code = String.valueOf((int)(Math.random() * 900000) + 100000); // code 6 chiffres
        codeMap.put(email, new CodeEntry(code, LocalDateTime.now().plusMinutes(5)));
        return code;
    }

    // Vérifier un code
    public boolean verifyCode(String email, String code) {
        CodeEntry entry = codeMap.get(email);
        if (entry == null) return false;
        if (entry.expiresAt.isBefore(LocalDateTime.now())) {
            codeMap.remove(email); // supprimer les expirés
            return false;
        }
        boolean valid = entry.code.equals(code);
        if (valid) codeMap.remove(email); // consommer le code après usage
        return valid;
    }
}

