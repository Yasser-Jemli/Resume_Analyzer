package org.example.Cv_Parser.controllers;

import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.dto.CVDto;
import org.example.Cv_Parser.models.Cv;
import org.example.Cv_Parser.services.CvService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.stream.Collectors;



@RestController
@RequestMapping("/api/cvs")
@RequiredArgsConstructor

public class CvController {
    private final CvService cvService;

    @GetMapping
    public List<CVDto> getAllCVs() {
        return cvService.getAllCvs().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @GetMapping("/{id}")
    public ResponseEntity<CVDto> getCVById(@PathVariable Long id) {
        Cv cv = cvService.getCvById(id);
        return cv != null ? ResponseEntity.ok(convertToDto(cv)) : ResponseEntity.notFound().build();
    }

    @PostMapping("/add_cv")
    public CVDto createCV(@RequestBody CVDto cvDto) {
        Cv cv = convertToEntity(cvDto);
        Cv savedCV = cvService.saveCv(cv);
        return convertToDto(savedCV);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCV(@PathVariable Long id) {
        cvService.deleteCv(id);
        return ResponseEntity.noContent().build();
    }

    // Helper methods to convert between CV and CVDto
    private CVDto convertToDto(Cv cv) {
        return new CVDto(
                cv.getId(),
                cv.getName(),
                cv.getEmail(),
                cv.getPhone(),
                cv.getSkills(),
                cv.getExperience(),
                cv.getEducation(),
                cv.getMissingRequiredSkills(),
                cv.getMissingPreferredSkills(),
                cv.getRelatedSkills(),
                cv.getHighPriorityLearningResources(),
                cv.getMediumPriorityLearningResources(),
                cv.getAdditionalLearningResources(),
                cv.getTotalScore(),
                cv.getSkillsScore(),
                cv.getExperienceScore(),
                cv.getEducationScore(),
                cv.getExperienceYears(),
                cv.getExperiencePositions(),
                cv.getExperienceDetails(),
                cv.getFeedback()
        );
    }

    private Cv convertToEntity(CVDto cvDto) {
        return new Cv(
                cvDto.getId(),
                cvDto.getName(),
                cvDto.getEmail(),
                cvDto.getPhone(),
                cvDto.getSkills(),
                cvDto.getExperience(),
                cvDto.getEducation(),
                cvDto.getMissingRequiredSkills(),
                cvDto.getMissingPreferredSkills(),
                cvDto.getRelatedSkills(),
                cvDto.getHighPriorityLearningResources(),
                cvDto.getMediumPriorityLearningResources(),
                cvDto.getAdditionalLearningResources(),
                cvDto.getTotalScore(),
                cvDto.getSkillsScore(),
                cvDto.getExperienceScore(),
                cvDto.getEducationScore(),
                cvDto.getExperienceYears(),
                cvDto.getExperiencePositions(),
                cvDto.getExperienceDetails(),
                cvDto.getFeedback()
        );
    }
}
