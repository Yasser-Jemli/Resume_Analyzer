package org.example.Cv_Parser.Security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
public class SecurityConfig {

    private final JwtAuthFilter jwtAuthFilter;
    private final UserDetailsService userDetailsService;

    public SecurityConfig(JwtAuthFilter jwtAuthFilter, UserDetailsService userDetailsService) {
        this.jwtAuthFilter = jwtAuthFilter;
        this.userDetailsService = userDetailsService;
    }

    // Define PasswordEncoder bean
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    // Security Filter Chain configuration
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(authorizeRequests ->
                        authorizeRequests
                                .requestMatchers("/api/auth/login", "/api/users").permitAll() // Public endpoints
                                // Restricted to SYSADMIN
                                .requestMatchers("/api/admin/**").hasRole("SYSADMIN")

                                // Restricted to MANAGER
                                .requestMatchers("/api/manager/**").hasRole("MANAGER")

                                // Restricted to CANDIDATE
                                .requestMatchers("/api/candidate/**").hasRole("CANDIDATE")
                                .anyRequest().authenticated() // Secured endpoints
                )
                .csrf(csrf -> csrf.disable()) // Disable CSRF protection (if using JWT)
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class); // Add JWT filter

        return http.build();
    }

    // Authentication Manager configuration
    @Bean
    public AuthenticationManager authenticationManager(HttpSecurity http) throws Exception {
        // Get AuthenticationManagerBuilder object
        var authenticationManagerBuilder = http.getSharedObject(AuthenticationManagerBuilder.class);

        // Configure authentication using userDetailsService and passwordEncoder
        authenticationManagerBuilder.userDetailsService(userDetailsService)
                .passwordEncoder(passwordEncoder());

        // Return the configured AuthenticationManager
        return authenticationManagerBuilder.build();
    }
}
