package org.example.Cv_Parser.Core.services;
import lombok.RequiredArgsConstructor;
import org.springframework.core.env.Environment;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;


@Service
@RequiredArgsConstructor


public class EmailService {
        private final JavaMailSender mailSender;
        private final Environment env;

        public void sendCredentialsEmail(String toEmail, String temporaryPassword) {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setFrom(env.getProperty("spring.mail.username"));
            message.setTo(toEmail);
            message.setSubject("Your Manager Account Credentials");
            message.setText(String.format(
                    "Welcome!\n\n" +
                            "Your temporary credentials:\n" +
                            "Email: %s\n" +
                            "Password: %s\n\n" +
                            "Please change your password after first login.",
                    toEmail, temporaryPassword
            ));
            mailSender.send(message);
        }
    }
