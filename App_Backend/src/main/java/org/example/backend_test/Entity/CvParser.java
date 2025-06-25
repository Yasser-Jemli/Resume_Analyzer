package org.example.backend_test.Entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class CvParser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long cvParserId;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String skillsJson;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String learningPathJson;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String skillRecommendationsJson;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String scoresJson;

    private String cvName;

    private String postName;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}
