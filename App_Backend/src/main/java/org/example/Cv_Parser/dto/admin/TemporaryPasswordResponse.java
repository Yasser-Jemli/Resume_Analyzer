package org.example.Cv_Parser.dto.admin;

public record TemporaryPasswordResponse(
        String email,
        String temporaryPassword
) {}
