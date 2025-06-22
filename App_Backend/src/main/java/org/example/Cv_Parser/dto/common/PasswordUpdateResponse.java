package org.example.Cv_Parser.dto.common;

import java.time.Instant;

public record PasswordUpdateResponse (
    String message,
    Instant timestamp
) {}

