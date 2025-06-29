package org.example.backend_test.Security;
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Date;

public class JwtTokenUtil {

    // Clé secrète (à stocker en config / env vars)
    private final Key secretKey;

    // Durée de validité du token (exemple 1h)
    private final long jwtExpirationInMs = 3600000;

    public JwtTokenUtil(String secret) {
        // Génère une clé à partir de la chaîne secrète (minimum 256 bits)
        this.secretKey = Keys.hmacShaKeyFor(secret.getBytes());
    }

    // Générer un token JWT
    public String generateToken(String username, String role) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + jwtExpirationInMs);

        return Jwts.builder()
                .setSubject(username)
                .claim("role", role)
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(secretKey, SignatureAlgorithm.HS256)
                .compact();
    }

    // Extraire le username depuis le token
    public String getUsernameFromJWT(String token) {
        Claims claims = Jwts.parserBuilder()
                .setSigningKey(secretKey)
                .build()
                .parseClaimsJws(token)
                .getBody();

        return claims.getSubject();
    }

    // Valider le token JWT
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException ex) {
            // Ici, log l'erreur si tu veux
            return false;
        }
    }
}

