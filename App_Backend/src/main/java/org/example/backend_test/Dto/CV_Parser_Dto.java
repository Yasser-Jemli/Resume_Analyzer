package org.example.backend_test.Dto;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.example.backend_test.Entity.CvParser;

import java.io.Serializable;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CV_Parser_Dto implements Serializable {
    private Long id;
    private String name;
    private String email;
    private String phone;
    private List<String> skills;
    private List<String> experience;
    private List<String> education;
    private List<String> missingRequiredSkills;
    private List<String> missingPreferredSkills;
    private List<String> relatedSkills;
    private List<String> highPriorityLearningResources;
    private List<String> mediumPriorityLearningResources;
    private List<String> additionalLearningResources;
    private Double totalScore;
    private Double skillsScore;
    private Double experienceScore;
    private Double educationScore;
    private Integer experienceYears;
    private Integer experiencePositions;
    private String experienceDetails;
    private List<String> feedback;
}

