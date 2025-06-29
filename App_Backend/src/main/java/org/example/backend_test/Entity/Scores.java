package org.example.backend_test.Entity;

import lombok.Data;

import java.util.List;
import java.util.Map;

public class Scores {
    private ScoreDetail pyres;

    @Data
    public static class ScoreDetail {
        private double total_score;
        private Map<String, Double> detailed_scores;
        private ExperienceMetrics experience_metrics;
        private List<String> feedback;
    }

    @Data
    public static class ExperienceMetrics {
        private int years;
        private int positions;
        private String details;
    }
}

