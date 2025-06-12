package org.example.Cv_Parser.admin.controller;

import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.dto.manager.ManagerCredentialRequest;
import org.example.Cv_Parser.admin.service.AdminService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {
    private final AdminService adminService;

    @PostMapping("/create-manager")
    @PreAuthorize("hasRole('SYSADMIN')")
    public ResponseEntity<String> createManagerAccount(
            @RequestBody ManagerCredentialRequest request) {
        adminService.createManagerAccount(request);
        return ResponseEntity.ok("Manager account created successfully");
    }
}
