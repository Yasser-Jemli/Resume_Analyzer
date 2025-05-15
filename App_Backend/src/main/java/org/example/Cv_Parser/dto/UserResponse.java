package org.example.Cv_Parser.dto;
import lombok.Data;
import org.example.Cv_Parser.models.UserRole;

@Data // Lombok will generate getters, setters, and other utility methods
public class UserResponse {
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private UserRole role;
}
