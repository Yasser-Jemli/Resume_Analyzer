package org.example.Cv_Parser.dto;


import lombok.Data;

@Data
public class AuthResponse {
    private String token;
    public AuthResponse(String token) { this.token = token; }
    public String getToken() { return token; }
}