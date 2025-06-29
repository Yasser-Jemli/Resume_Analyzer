package org.example.backend_test.Dto;
import lombok.Getter;
import lombok.Setter;
import org.example.backend_test.Entity.User;

@Getter
@Setter
public class UserDTO {
    private Long id;
    private String username;
    private String email;
    private String role;

    public UserDTO(User user) {
        this.id = user.getId();
        this.username = user.getUsername();
        this.email = user.getEmail();
        this.role = user.getRole().toString();
    }

    // getters
}
