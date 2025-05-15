package org.example.Cv_Parser.services;

import org.example.Cv_Parser.repositories.UserRepository;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(); // Use the same encoder

    @Override
    public org.springframework.security.core.userdetails.UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        // Fetch the user from the database
        org.example.Cv_Parser.models.User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        // Return a Spring Security User object with the encoded password
        return new org.springframework.security.core.userdetails.User(
                user.getEmail(),
                user.getPassword(), // This is the encoded password
                new ArrayList<>()  // Authorities or roles can go here
        );
    }
}
