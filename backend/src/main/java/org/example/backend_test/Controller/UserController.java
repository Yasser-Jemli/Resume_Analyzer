package org.example.backend_test.Controller;

import org.example.backend_test.Dto.UserDTO;
import org.example.backend_test.Entity.User;
import org.example.backend_test.Security.JwtTokenUtil;
import org.example.backend_test.Service.ConfirmationCodeService;
import org.example.backend_test.Service.EmailService;
import org.example.backend_test.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import java.util.List;
import java.util.Map;
import java.util.Optional;
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
        this.jwtUtil = new JwtTokenUtil("ta_clef_secrete_qui_doivent_etre_longue_et_secrete");
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
        } else { return ResponseEntity.ok(Map.of("exists", false));
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
    public ResponseEntity<User> signupUser(@RequestBody @Valid User newUser) {
        User savedUser = userService.saveUser(newUser);
        return ResponseEntity.ok(savedUser);
    }

    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@RequestBody User loginRequest) {
        // Validation simple des champs
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

        // Recherche user par username ou email
        Optional<User> userOpt = (loginRequest.getUsername() != null && !loginRequest.getUsername().isEmpty())
                ? userService.findByUsername(loginRequest.getUsername())
                : userService.findByEmail(loginRequest.getEmail());

        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "User not found"
            ));
        }

        User user = userOpt.get();

        // Vérification password (attention ici pas de hash, à améliorer)
        if (!user.getPassword().equals(loginRequest.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "success", false,
                    "message", "Invalid password"
            ));
        }

        String token = jwtUtil.generateToken(user.getUsername(), String.valueOf(user.getRole()));

        Boolean mustChangePwd = user.getMustChangePassword();
        if (mustChangePwd == null) {
            mustChangePwd = false;
        }

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
            System.out.println("code de confirmation"+code);
            return ResponseEntity.ok(Map.of("message", "Code envoyé"));
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("error", "Utilisateur non trouvé"));
        }
    }

    @PostMapping("/verify-code")
    public ResponseEntity<?> verifyCode(@RequestBody Map<String, String> data) {
        String email = data.get("email");
        String code = data.get("code");

        if (codeService.verifyCode(email, code)) {
            return ResponseEntity.ok(Map.of("message", "Code confirmé"));
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("error", "Code invalide ou expiré"));
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
