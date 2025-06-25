package org.example.backend_test.Service;

import org.springframework.stereotype.Service;

@Service
public class EmailService {
    public void sendConfirmationCode(String to, String code) {
        System.out.println("Envoi du code " + code + " à " + to);
        // Implémentation réelle : JavaMailSender ou autre
    }
}
