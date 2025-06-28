package org.example.backend_test.Security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtUtil jwtUtil;

    public JwtAuthFilter(JwtUtil jwtUtil) {
        this.jwtUtil = jwtUtil;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        try {
            String token = getJwtFromRequest(request);

            // Add debug logging
            System.out.println("JWT Token found: " + (token != null));

            if (token != null && jwtUtil.validateToken(token)) {
                String email = jwtUtil.extractUsername(token);
                String role = jwtUtil.extractRole(token);

                // Add debug logging
                System.out.println("Authenticating user: " + email + " with role: " + role);

                if (email == null || role == null) {
                    throw new RuntimeException("Missing required claims in token");
                }

                // Normalize role to always include ROLE_ prefix
                String authority = role.startsWith("ROLE_") ? role : "ROLE_" + role;

                // Create UserDetails object with proper authorities
                UserDetails userDetails = User.builder()
                        .username(email)
                        .password("") // Password not needed for JWT auth
                        .authorities(authority)
                        .build();

                // Create authentication token with UserDetails
                UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                        userDetails, // Principal should be UserDetails
                        null,        // Credentials
                        userDetails.getAuthorities()
                );

                // Set authentication in security context
                SecurityContextHolder.getContext().setAuthentication(auth);

                // Debug log
                System.out.println("Authentication set successfully for: " + email);
            }
        } catch (Exception e) {
            // Enhanced error logging
            System.err.println("JWT Authentication failed: " + e.getMessage());
            SecurityContextHolder.clearContext();
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Authentication failed: " + e.getMessage());
            return;
        }
        filterChain.doFilter(request, response);
    }

    private String getJwtFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}