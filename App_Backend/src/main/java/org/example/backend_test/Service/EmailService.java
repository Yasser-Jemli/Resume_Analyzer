package org.example.backend_test.Service;

import lombok.RequiredArgsConstructor;
import org.example.backend_test.Entity.User;
import org.springframework.core.env.Environment;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor

public class EmailService {

    private final JavaMailSender mailSender;
    private final Environment env;

    public void sendVerificationEmail(User user, String verificationCode) {
        String verificationLink = "http://localhost:8081/auth/verify-code?code=" + verificationCode;
        // Simple email content
        String content = "Dear " + user.getUsername() + ",\n\n"
                + "Please click the link below to verify your email:\n"
                + verificationLink;
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom(env.getProperty("spring.mail.username"));
        message.setTo(user.getEmail());
        message.setText(content);
        mailSender.send(message);
    }
    public void sendConfirmationCode(String to, String code) {
        System.out.println("Envoi du code " + code + " à " + to);
        // Implémentation réelle : JavaMailSender ou autre
    }

}
