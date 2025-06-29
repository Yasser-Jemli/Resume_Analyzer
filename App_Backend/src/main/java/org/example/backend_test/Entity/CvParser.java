package org.example.backend_test.Entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CvParser implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "cv_parser_id")  // Explicit column name
    private Long cvParserId;

    private String name;
    private String email;
    private String phone;

    @ElementCollection
    @CollectionTable(name = "cv_parser_skills",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "skill")
    private List<String> skills;

    @ElementCollection
    @CollectionTable(name = "cv_parser_experience",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "experience")
    private List<String> experience;

    @ElementCollection
    @CollectionTable(name = "cv_parser_education",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "education")
    private List<String> education;

    @ElementCollection
    @CollectionTable(name = "cv_parser_missing_skills",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "missing_required_skill")
    private List<String> missingRequiredSkills;

    @ElementCollection
    @CollectionTable(name = "cv_parser_preferred_skills",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "missing_preferred_skill")
    private List<String> missingPreferredSkills;

    @ElementCollection
    @CollectionTable(name = "cv_parser_related_skills",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "related_skill")
    private List<String> relatedSkills;

    @ElementCollection
    @CollectionTable(name = "cv_parser_high_priority_resources",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "high_priority_resource")
    private List<String> highPriorityLearningResources;

    @ElementCollection
    @CollectionTable(name = "cv_parser_medium_priority_resources",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "medium_priority_resource")
    private List<String> mediumPriorityLearningResources;

    @ElementCollection
    @CollectionTable(name = "cv_parser_additional_resources",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "additional_resource")
    private List<String> additionalLearningResources;

    private Double totalScore;
    private Double skillsScore;
    private Double experienceScore;
    private Double educationScore;

    private Integer experienceYears;
    private Integer experiencePositions;
    private String experienceDetails;

    @ElementCollection
    @CollectionTable(name = "cv_parser_feedback",
            joinColumns = @JoinColumn(name = "cv_parser_id"))
    @Column(name = "feedback")
    private List<String> feedback;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}