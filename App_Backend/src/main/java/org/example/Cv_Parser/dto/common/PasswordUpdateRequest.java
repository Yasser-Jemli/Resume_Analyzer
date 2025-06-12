package org.example.Cv_Parser.dto.common;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public record PasswordUpdateRequest(
        @NotBlank @Email String email,
        @NotBlank   String currentPassword,
        @NotBlank  String newPassword
) {}

