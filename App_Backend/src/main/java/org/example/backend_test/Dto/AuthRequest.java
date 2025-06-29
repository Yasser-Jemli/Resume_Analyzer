package org.example.backend_test.Dto;

import lombok.Data;

@Data
public class AuthRequest {
    private String username;
    private String password;

}