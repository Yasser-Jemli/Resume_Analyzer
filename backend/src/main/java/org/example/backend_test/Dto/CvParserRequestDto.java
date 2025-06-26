package org.example.backend_test.Dto;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CvParserRequestDto {
    private Object cv_name;
    private Object skills;
    private Object learning_path;
    private Object skill_recommendations;
    private Object scores;
}
