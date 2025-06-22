package org.example.Cv_Parser.manager;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.Core.exceptions.CustomExceptions;
import org.example.Cv_Parser.Core.models.User;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ManagerService {

    private final ManagerRepository managerRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public void updatePassword(String email,
                               String currentPassword,
                               String newPassword) {

        User manager = managerRepository.findByEmail(email)
                .orElseThrow(() -> new CustomExceptions.ManagerNotFoundException(email));

        // Only verify current password matches
        if (!passwordEncoder.matches(currentPassword, manager.getPassword())) {
            throw new CustomExceptions.InvalidCurrentPasswordException();
        }

        // Directly update without validation
        manager.setPassword(passwordEncoder.encode(newPassword));
        manager.setPasswordChanged(true);
        managerRepository.save(manager);
    }
}