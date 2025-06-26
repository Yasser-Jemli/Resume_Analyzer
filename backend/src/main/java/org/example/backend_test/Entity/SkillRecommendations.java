package org.example.backend_test.Entity;

import lombok.Data;

import java.util.List;

public class SkillRecommendations {
    private String status;
    private String position;
    private List<String> current_skills;
    private RecommendationDetails recommendations;

    @Data
    public static class RecommendationDetails {
        private List<String> missing_required;
        private List<String> missing_preferred;
        private List<String> related_skills;
        private List<SkillPathItem> skill_path;
    }

    @Data
    public static class SkillPathItem {
        private String skill;
        private String priority;
        private String reason;
    }
}
