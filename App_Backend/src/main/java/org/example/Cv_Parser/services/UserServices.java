package org.example.Cv_Parser.services;

import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.dto.CreateUserRequest;
import org.example.Cv_Parser.dto.UserResponse;
import org.example.Cv_Parser.models.User;
import org.example.Cv_Parser.repositories.UserRepository;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;


@Service
@RequiredArgsConstructor
public class UserServices {
    private final UserRepository userRepository;

    public UserResponse createUser(CreateUserRequest request) {
        // Create an encoder instance
        BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

        // Encode the plain text password
        String encodedPassword = passwordEncoder.encode(request.getPassword());

        User user = User.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail())
                .password(encodedPassword) // Hash this later
                .role(request.getRole())
                .build();

        User saved = userRepository.save(user);

        // Generate UserResponse using Lombok-generated getters
        UserResponse response = new UserResponse();
        response.setId(saved.getId());
        response.setFirstName(saved.getFirstName());
        response.setLastName(saved.getLastName());
        response.setEmail(saved.getEmail());
        response.setRole(saved.getRole());

        return response;
    }
    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found"));

        UserResponse response = new UserResponse();
        response.setId(user.getId());
        response.setFirstName(user.getFirstName());
        response.setLastName(user.getLastName());
        response.setEmail(user.getEmail());
        response.setRole(user.getRole());

        return response;
    }

    public static class UserNotFoundException extends RuntimeException {
        public UserNotFoundException(String message) {
            super(message);
        }
    }


    public List<UserResponse> getAllUsers() {
        List<User> users = userRepository.findAll();

        return users.stream().map(user -> {
            UserResponse response = new UserResponse();
            response.setId(user.getId());
            response.setFirstName(user.getFirstName());
            response.setLastName(user.getLastName());
            response.setEmail(user.getEmail());
            response.setRole(user.getRole());
            return response;
        }).collect(Collectors.toList());
    }
    public UserResponse updateUser(Long id, CreateUserRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Update fields
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setEmail(request.getEmail());
        user.setRole(request.getRole());

        // Hash the password if the password is being updated
        if (request.getPassword() != null && !request.getPassword().isEmpty()) {
            BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
            user.setPassword(passwordEncoder.encode(request.getPassword())); // Hash the password
        }

        User updatedUser = userRepository.save(user);

        UserResponse response = new UserResponse();
        response.setId(updatedUser.getId());
        response.setFirstName(updatedUser.getFirstName());
        response.setLastName(updatedUser.getLastName());
        response.setEmail(updatedUser.getEmail());
        response.setRole(updatedUser.getRole());

        return response;
    }
    public void deleteUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));

        userRepository.delete(user);
    }

}
