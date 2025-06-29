package org.example.backend_test.Controller;

import org.example.backend_test.Dto.AuthRequest;
import org.example.backend_test.Dto.UserDTO;
import org.example.backend_test.Entity.Role;
import org.example.backend_test.Entity.User;
import org.example.backend_test.Security.JwtUtil;
import org.example.backend_test.Service.ConfirmationCodeService;
import org.example.backend_test.Service.EmailService;
import org.example.backend_test.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.Email;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/auth")
@Validated
public class UserController {
    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;

    private final UserService userService;

    @Autowired
    private ConfirmationCodeService codeService;

    @Autowired
    private EmailService emailService;
    // Injecter via constructeur (plus propre)

    @Autowired
    public UserController(AuthenticationManager authenticationManager, JwtUtil jwtUtil, UserService userService) {
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
        this.userService = userService;
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
    public ResponseEntity<User> signupUser (@RequestBody @Valid User newUser ) {
        String verificationCode = UUID.randomUUID().toString();
        newUser.setEnabled(false);
        User savedUser  = userService.saveUser (newUser );
        emailService.sendVerificationEmail(savedUser,verificationCode ); // Send verification email
        return ResponseEntity.ok(savedUser );
    }

    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@RequestBody AuthRequest loginRequest) {
        System.out.println("Login attempt for: " + loginRequest.getUsername());
        try {
            // Authenticate
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            loginRequest.getUsername(),
                            loginRequest.getPassword()
                    )
            );
            System.out.println("Authentication successful!");
            UserDetails userDetails = (UserDetails) authentication.getPrincipal();
// Extract role from authorities
            String role = userDetails.getAuthorities().stream()
                    .map(GrantedAuthority::getAuthority)
                    .findFirst()
                    .orElse("ROLE_USER");

            // Generate token
            String token = jwtUtil.generateToken(
                    loginRequest.getUsername(),
                    Role.valueOf(role.replace("ROLE_", ""))
            );
            System.out.println("Generated token: " + token);

            // Return response
            return ResponseEntity.ok()
                    .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
                    .body(Map.of(
                            "token", token,
                            "username", loginRequest.getUsername(),
                            "role", role
                    ));

        } catch (BadCredentialsException e) {
            System.out.println("Authentication failed for: " + loginRequest.getUsername());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "Invalid email or password"));
        }
    }


//        // Validation simple des champs
//        if ((loginRequest.getUsername() == null || loginRequest.getUsername().isEmpty()) &&
//                (loginRequest.getUsername() == null || loginRequest.getUsername().isEmpty())) {
//            return ResponseEntity.badRequest().body(Map.of(
//                    "success", false,
//                    "message", "Username or email is required"
//            ));
//        }
//        if (loginRequest.getPassword() == null || loginRequest.getPassword().isEmpty()) {
//            return ResponseEntity.badRequest().body(Map.of(
//                    "success", false,
//                    "message", "Password is required"
//            ));
//        }
//
//        // Recherche user par username ou email
//        Optional<User> userOpt = (loginRequest.getUsername() != null && !loginRequest.getUsername().isEmpty())
//                ? userService.findByUsername(loginRequest.getUsername())
//                : userService.findByEmail(loginRequest.getUsername());
//
//        if (userOpt.isEmpty()) {
//            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
//                    "success", false,
//                    "message", "User not found"
//            ));
//        }
//    }

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
    public ResponseEntity<?> verifyUser (@RequestParam("code") String code) {
        if (userService.verifyUser (code)) {
            return ResponseEntity.ok(Map.of("message", "Verification successful. You can now log in."));
        } else {
            return ResponseEntity.badRequest().body(Map.of("error", "Invalid or expired verification code."));
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
