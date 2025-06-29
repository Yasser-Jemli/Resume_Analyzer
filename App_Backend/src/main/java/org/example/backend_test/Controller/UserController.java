package org.example.backend_test.Controller;

import org.example.backend_test.Dto.UserDTO;
import org.example.backend_test.Entity.User;
import org.example.backend_test.Security.JwtTokenUtil;
import org.example.backend_test.Security.PasswordUtils;
import org.example.backend_test.Service.ConfirmationCodeService;
import org.example.backend_test.Service.EmailService;
import org.example.backend_test.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.Email;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/auth")
@Validated
public class UserController {

    private final UserService userService;
    private final JwtTokenUtil jwtUtil;

    @Autowired
    private ConfirmationCodeService codeService;

    @Autowired
    private EmailService emailService;
    // Injecter via constructeur (plus propre)

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;

        // Idéalement, injecter via configuration/Bean
        this.jwtUtil = new JwtTokenUtil("f01d2052c57aa5e2454f42701378138b741876951ec571f1230d8dc2b0e6f325");
    }

    @GetMapping("/check-email")
    public ResponseEntity<?> checkEmailExists(@RequestParam("email") @Email String email) {
        Optional<User> userOptional = userService.findByEmail(email);

        if (userOptional.isPresent()) {
            User user = userOptional.get();

            // Replace with actual logic to generate token and determine if password must be changed

            Map<String, Object> response = Map.of(
                    "exists", true,
                    "id", user.getId(),
                    "username", user.getUsername(),
                    "email", user.getEmail(),
                    "role", user.getRole()
            );

            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.ok(Map.of("exists", false));
        }
    }


    @GetMapping("/check-username")
    public ResponseEntity<Map<String, Boolean>> checkUsernameExists(@RequestParam("username") String username) {
        boolean exists = userService.findByUsername(username).isPresent();
        // Si l'utilisateur est trouvé, exists = true, sinon false
        return ResponseEntity.ok(Map.of("exists", exists));
    }

    @GetMapping("/getallusers")
    public ResponseEntity<List<UserDTO>> getAllUsers() {
        List<UserDTO> userDTOs = userService.getAllUsers().stream()
                .map(UserDTO::new)
                .collect(Collectors.toList());

        return ResponseEntity.ok(userDTOs);
    }


    @PostMapping("/signup")
    public ResponseEntity<?> signupUser(@RequestBody @Valid User newUser) {
        try {
            // 1. Validate password isn't already hashed
            if (newUser.getPassword().startsWith("$2a$")) {
                return ResponseEntity.badRequest().body(
                        Map.of(
                                "success", false,
                                "message", "Password appears to be already hashed"
                        )
                );
            }

            // 2. Check email availability
            if (userService.existsByEmail(newUser.getEmail())) {
                return ResponseEntity.badRequest().body(
                        Map.of(
                                "success", false,
                                "message", "Email is already registered"
                        )
                );
            }

            // Hash and save user
            String rawPassword = newUser.getPassword().trim();
            String salt = PasswordUtils.generateSalt();
            String hashedPassword = PasswordUtils.hashPassword(rawPassword, salt);
            newUser.setPassword(hashedPassword);
            newUser.setEnabled(false);
            newUser.setVerificationCode(UUID.randomUUID().toString());

            User savedUser = userService.saveUser(newUser);

            // 5. Verify storage

            // 6. Send verification email
            emailService.sendVerificationEmail(savedUser, savedUser.getVerificationCode());

            return ResponseEntity.ok(
                    Map.of(
                            "success", true,
                            "message", "Registration successful",
                            "userId", savedUser.getId()
                    )
            );

        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(
                    Map.of(
                            "success", false,
                            "message", "Registration failed: " + e.getMessage()
                    )
            );
        }
    }
    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@RequestBody User loginRequest) {

        // Input validation
        if ((loginRequest.getUsername() == null || loginRequest.getUsername().isEmpty()) &&
                (loginRequest.getEmail() == null || loginRequest.getEmail().isEmpty())) {
            return ResponseEntity.badRequest().body(Map.of(
                    "success", false,
                    "message", "Username or email is required"
            ));
        }

        if (loginRequest.getPassword() == null || loginRequest.getPassword().isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "success", false,
                    "message", "Password is required"
            ));
        }


        // Find user
        Optional<User> userOpt = (loginRequest.getUsername() != null && !loginRequest.getUsername().isEmpty())
                ? userService.findByUsername(loginRequest.getUsername())
                : userService.findByEmail(loginRequest.getEmail());

        System.out.println("Login attempt for: " +
                (loginRequest.getUsername() != null ? loginRequest.getUsername() : loginRequest.getEmail()));
        System.out.println("Raw password received: " + loginRequest.getPassword());

        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "Invalid credentials 1" // Keep generic for security
            ));
        }


        User user = userOpt.get();
        System.out.println("Found user: " + user.getUsername());
        System.out.println("Stored password hash: " + user.getPassword());
        System.out.println("Account enabled: " + user.getEnabled());

        // Account verification check
        if (!user.getEnabled()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "Account not verified. Please check your email."
            ));
        }
        // Password verification using SHA-256
        if (!PasswordUtils.verifyPassword(loginRequest.getPassword(), user.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "Invalid credentials"
            ));
        }

        // Generate token using your existing JWT util
        String token = jwtUtil.generateToken(user.getUsername(), String.valueOf(user.getRole()));
        Boolean mustChangePwd = user.getMustChangePassword();
        if (mustChangePwd == null) {
            mustChangePwd = false;
        }
        // Build response
        return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Login successful",
                "id", user.getId(),
                "username", user.getUsername(),
                "email", user.getEmail(),
                "token", token,
                "role", user.getRole(),
                "mustChangePassword", mustChangePwd
        ));

    }

    @DeleteMapping("/deleteUser/{id}")
    public ResponseEntity<Map<String, Object>> deleteUser(@PathVariable Long id) {
        try {
            boolean deleted = userService.deleteUserById(id);
            if (deleted) {
                return ResponseEntity.ok(Map.of("success", true, "message", "User deleted successfully"));
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("success", false, "message", "User not found"));
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("success", false, "message", "Internal server error"));
        }
    }

    public static class PasswordUpdateRequest {
        public String newPassword;
    }

    @PatchMapping("/updatePassword/{id}")
    public ResponseEntity<?> updatePassword(@PathVariable Long id, @RequestBody Map<String, String> body) {
        String newPassword = body.get("newPassword");
        if (newPassword == null || newPassword.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("message", "New password is required"));
        }

        try {
            boolean updated = userService.updatePassword(id, newPassword);
            if (updated) {
                return ResponseEntity.ok(Map.of("success", true, "message", "Password updated successfully"));
            } else {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("success", false, "message", "User not found"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of("success", false, "message", "Server error"));
        }
    }

    @GetMapping("/getPassword/{id}")
    public ResponseEntity<?> getPasswordByUserId(@PathVariable Long id) {
        Optional<User> userOpt = userService.findById(id);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            return ResponseEntity.ok(Map.of("password", user.getPassword()));
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("message", "User not found"));
        }
    }

    @PostMapping("/resend-code")
    public ResponseEntity<?> resendConfirmationCode(@RequestBody Map<String, String> data) {
        String email = data.get("email");
        Optional<User> optionalUser = userService.findByEmail(email);

        if (optionalUser.isPresent()) {
            String code = codeService.generateAndStoreCode(email);
            emailService.sendConfirmationCode(email, code);
            System.out.println("code de confirmation" + code);
            return ResponseEntity.ok(Map.of("message", "Code envoyé"));
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("error", "Utilisateur non trouvé"));
        }
    }

    @GetMapping("/verify-code")
    public ResponseEntity<String> verifyUser(@RequestParam String code) {
        try {
            userService.verifyUser(code);
            return ResponseEntity.ok("Account verified successfully");
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @PostMapping("/send-login-code")
    public ResponseEntity<?> sendLoginCode(@RequestBody Map<String, String> data) {
        String email = data.get("email");

        if (email == null || email.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Email is required"));
        }

        // Directly send code — no DB check
        String code = codeService.generateAndStoreCode(email);
        emailService.sendConfirmationCode(email, code);
        System.out.println("Temporary login code sent to: " + email);

        return ResponseEntity.ok(Map.of("message", "Code envoyé"));
    }

}

