package org.example.Cv_Parser.admin.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.dto.manager.ManagerCredentialRequest;
import org.example.Cv_Parser.Core.models.User;
import org.example.Cv_Parser.Core.models.UserRole;
import org.example.Cv_Parser.Core.repositories.UserRepository;
import org.example.Cv_Parser.Core.services.EmailService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AdminService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    @Transactional
    public void createManagerAccount(ManagerCredentialRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new IllegalArgumentException("Email already exists");
        }

        User manager = new User();
        manager.setFirstName(request.firstName()); // Set first name
        manager.setLastName(request.lastName());   // Set last name
        manager.setEmail(request.email());
        manager.setPassword(passwordEncoder.encode(request.temporaryPassword()));
        manager.setRole(UserRole.MANAGER);
        manager.setPasswordChanged(false); // Add this field to User entity

        userRepository.save(manager);
        emailService.sendCredentialsEmail(request.email(), request.temporaryPassword());
    }
}

