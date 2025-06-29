package org.example.Cv_Parser.dto;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public class CVDto {
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

