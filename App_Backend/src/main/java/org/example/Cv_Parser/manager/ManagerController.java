package org.example.Cv_Parser.manager;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.dto.common.PasswordUpdateRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.Map;

@RestController
@RequestMapping("/api/managers")
@RequiredArgsConstructor
public class ManagerController {

    private final ManagerService managerService;

    @PostMapping("/update-password")
    @PreAuthorize("hasRole('MANAGER')")
    public ResponseEntity<Map<String, String>> updatePassword(
            @RequestBody @Valid PasswordUpdateRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {

        // 1. Check if user is authenticated
        if (userDetails == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Collections.singletonMap("error", "Authentication required"));
        }
        // 2. Verify the authenticated user matches the request
        if (!userDetails.getUsername().equals(request.email())) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(Collections.singletonMap("error", "Unauthorized password update attempt"));
        }

        try {
            // 3. Process the password update
            managerService.updatePassword(
                    request.email(),
                    request.currentPassword(),
                    request.newPassword()
            );

            return ResponseEntity.ok(Collections.singletonMap(
                    "message", "Password updated successfully"
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Collections.singletonMap("error", "Failed to update password"));
        }
    }
}



