package org.example.backend_test.Service;

import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
public class EmailService {

    private final JavaMailSender mailSender;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void sendConfirmationCode(String to, String code) {
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(to);
            message.setSubject("Your Verification Code");
            message.setText("Your verification code is: " + code);

            mailSender.send(message);
            System.out.println("Confirmation code sent to " + to);
        } catch (Exception e) {
            System.err.println("Failed to send confirmation code to " + to);
            e.printStackTrace();
            // Consider throwing a custom exception or handling it appropriately
        }
    }
}