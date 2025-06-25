package org.example.backend_test.Service;

import org.example.backend_test.Entity.User;
import org.example.backend_test.Repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final ConfirmationCodeService confirmationCodeService;
    private final EmailService emailService;

    public UserService(UserRepository userRepository,
                       ConfirmationCodeService confirmationCodeService,
                       EmailService emailService) {
        this.userRepository = userRepository;
        this.confirmationCodeService = confirmationCodeService;
        this.emailService = emailService;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public Optional<User> authenticateUser(String username, String email, String password) {
        return userRepository.findByUsernameOrEmailAndPassword(username, email, password);
    }

    public boolean existsByEmail(String email) {
        return userRepository.findByEmail(email).isPresent();
    }

    public boolean existsByUsername(String username) {
        return userRepository.findByUsername(username).isPresent();
    }

    public User saveUser(User user) {
        return userRepository.save(user);
    }

    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    public boolean deleteUserById(Long id) {
        Optional<User> userOpt = userRepository.findById(id);
        if (userOpt.isPresent()) {
            User user = userOpt.get();

            if (user.getMustChangePassword() == null) {
                user.setMustChangePassword(false);
                userRepository.save(user);
            }

            userRepository.deleteById(id);
            return true;
        }
        return false;
    }

    public boolean updatePassword(Long id, String newPassword) {
        Optional<User> optionalUser = userRepository.findById(id);
        if (optionalUser.isPresent()) {
            User user = optionalUser.get();
            user.setPassword(newPassword);
            user.setMustChangePassword(false);
            userRepository.save(user);
            return true;
        }
        return false;
    }

    // ➕ Nouveau : envoie un code temporaire (en mémoire) à l'utilisateur
    public boolean resendConfirmationCode(String email) {
        Optional<User> optionalUser = userRepository.findByEmail(email);
        if (optionalUser.isPresent()) {
            String code = confirmationCodeService.generateAndStoreCode(email);
            emailService.sendConfirmationCode(email, code);
            return true;
        }
        return false;
    }

    // ➕ Nouveau : vérifie le code temporaire (depuis mémoire)
    public boolean verifyConfirmationCode(String email, String code) {
        return confirmationCodeService.verifyCode(email, code);
    }
}
