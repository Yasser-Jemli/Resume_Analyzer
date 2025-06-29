package org.example.backend_test.Service;

import lombok.RequiredArgsConstructor;
import org.example.backend_test.Entity.User;
import org.example.backend_test.Repository.UserRepository;
import org.example.backend_test.Security.PasswordUtils;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final ConfirmationCodeService confirmationCodeService;
    private final EmailService emailService;


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
        // Generate salt and hash the password
        if (!user.getPassword().contains(":")) { // Ensure it's not already hashed
            String salt = PasswordUtils.generateSalt();
            String hashedPassword = PasswordUtils.hashPassword(user.getPassword(), salt);
            user.setPassword(hashedPassword);
        }

        user.setEnabled(false);
        user.setVerificationCode(UUID.randomUUID().toString());
        user.setMustChangePassword(false);

        User savedUser = userRepository.save(user);
        emailService.sendVerificationEmail(savedUser, savedUser.getVerificationCode());

        return savedUser;
    }


    public void verifyUser(String verificationCode) {
        User user = findByVerificationCode(verificationCode);
        if (user.getEnabled()) {
            throw new RuntimeException("Account already verified");
        }
        user.setVerificationCode(null);
        user.setEnabled(true);
        userRepository.save(user);
    }
    public Optional<User> findByUsername(String username) {
        // Add logging to verify the lookup
        System.out.println("Searching for username: " + username);
        Optional<User> user = userRepository.findByUsername(username);
        user.ifPresent(u -> System.out.println("Found user: " + u.getEmail()));
        return user;
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
    public User findByVerificationCode(String verificationCode) {
        return userRepository.findByVerificationCode(verificationCode)
                .orElseThrow(() -> new RuntimeException("Invalid verification code: " + verificationCode));
    }
}
