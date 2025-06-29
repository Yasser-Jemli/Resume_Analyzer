package org.example.Cv_Parser.models;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;


@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Cv {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String email;
    private String phone;

    @ElementCollection
    private List<String> skills;

    @ElementCollection
    private List<String> experience;

    @ElementCollection
    private List<String> education;

    @ElementCollection
    private List<String> missingRequiredSkills;

    @ElementCollection
    private List<String> missingPreferredSkills;

    @ElementCollection
    private List<String> relatedSkills;

    @ElementCollection
    private List<String> highPriorityLearningResources;

    @ElementCollection
    private List<String> mediumPriorityLearningResources;

    @ElementCollection
    private List<String> additionalLearningResources;

    private Double totalScore;
    private Double skillsScore;
    private Double experienceScore;
    private Double educationScore;

    private Integer experienceYears;
    private Integer experiencePositions;
    private String experienceDetails;

    @ElementCollection
    private List<String> feedback;
}
