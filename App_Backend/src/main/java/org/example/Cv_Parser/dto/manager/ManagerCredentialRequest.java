package org.example.Cv_Parser.dto.manager;

import org.example.Cv_Parser.Core.models.UserRole;

public record ManagerCredentialRequest(
        String firstName,
        String lastName,
        String email,
        String temporaryPassword,
        UserRole role) {}

