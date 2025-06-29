package org.example.backend_test.Controller;

import lombok.RequiredArgsConstructor;
import org.example.backend_test.Dto.CV_Parser_Dto;
import org.example.backend_test.Entity.CvParser;
import org.example.backend_test.Service.CvParserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/cv-parser")
@RequiredArgsConstructor
public class CvParserController {

    private final CvParserService cvParserService;

    @GetMapping
    public List<CV_Parser_Dto> getAllCVs() {
        return cvParserService.getAllCvs().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    @GetMapping("/{id}")
    public ResponseEntity<CV_Parser_Dto> getCVById(@PathVariable Long id) {
        return cvParserService.getCvById(id)
                .map(this::convertToDto)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/add_Parsed_cv")
    public ResponseEntity<CV_Parser_Dto> createCV(@RequestBody CV_Parser_Dto cvDto) {
        CvParser cv = convertToEntity(cvDto);
        CvParser savedCV = cvParserService.saveCv(cv);
        return ResponseEntity.ok(convertToDto(savedCV));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCV(@PathVariable Long id) {
        cvParserService.deleteCv(id);
        return ResponseEntity.noContent().build();
    }
    @GetMapping("/by-skill")
    public ResponseEntity<List<CvParser>> getBySkill(
            @RequestParam String skill) {
        return ResponseEntity.ok(cvParserService.findBySkill(skill));
    }

    @GetMapping("/by-skills")
    public ResponseEntity<List<CvParser>> getBySkills(
            @RequestParam List<String> skills) {
        return ResponseEntity.ok(cvParserService.findBySkills(skills));
    }

    @GetMapping("/skills/unique")
    public ResponseEntity<List<String>> getAllUniqueSkills() {
        return ResponseEntity.ok(cvParserService.findAllUniqueSkills());
    }

    @GetMapping("/skills/stats")
    public ResponseEntity<Map<String, Long>> getSkillStatistics() {
        return ResponseEntity.ok(cvParserService.getSkillStatistics());
    }


    // Helper methods
    private CV_Parser_Dto convertToDto(CvParser cv) {
        CV_Parser_Dto dto = new CV_Parser_Dto();
        dto.setId(cv.getCvParserId());
        dto.setName(cv.getName());
        dto.setEmail(cv.getEmail());
        dto.setPhone(cv.getPhone());
        dto.setSkills(cv.getSkills());
        dto.setExperience(cv.getExperience());
        dto.setEducation(cv.getEducation());
        dto.setMissingRequiredSkills(cv.getMissingRequiredSkills());
        dto.setMissingPreferredSkills(cv.getMissingPreferredSkills());
        dto.setRelatedSkills(cv.getRelatedSkills());
        dto.setHighPriorityLearningResources(cv.getHighPriorityLearningResources());
        dto.setMediumPriorityLearningResources(cv.getMediumPriorityLearningResources());
        dto.setAdditionalLearningResources(cv.getAdditionalLearningResources());
        dto.setTotalScore(cv.getTotalScore());
        dto.setSkillsScore(cv.getSkillsScore());
        dto.setExperienceScore(cv.getExperienceScore());
        dto.setEducationScore(cv.getEducationScore());
        dto.setExperienceYears(cv.getExperienceYears());
        dto.setExperiencePositions(cv.getExperiencePositions());
        dto.setExperienceDetails(cv.getExperienceDetails());
        dto.setFeedback(cv.getFeedback());
        return dto;
    }

    private CvParser convertToEntity(CV_Parser_Dto dto) {
        CvParser cv = new CvParser();
        cv.setCvParserId(dto.getId());
        cv.setName(dto.getName());
        cv.setEmail(dto.getEmail());
        cv.setPhone(dto.getPhone());
        cv.setSkills(dto.getSkills());
        cv.setExperience(dto.getExperience());
        cv.setEducation(dto.getEducation());
        cv.setMissingRequiredSkills(dto.getMissingRequiredSkills());
        cv.setMissingPreferredSkills(dto.getMissingPreferredSkills());
        cv.setRelatedSkills(dto.getRelatedSkills());
        cv.setHighPriorityLearningResources(dto.getHighPriorityLearningResources());
        cv.setMediumPriorityLearningResources(dto.getMediumPriorityLearningResources());
        cv.setAdditionalLearningResources(dto.getAdditionalLearningResources());
        cv.setTotalScore(dto.getTotalScore());
        cv.setSkillsScore(dto.getSkillsScore());
        cv.setExperienceScore(dto.getExperienceScore());
        cv.setEducationScore(dto.getEducationScore());
        cv.setExperienceYears(dto.getExperienceYears());
        cv.setExperiencePositions(dto.getExperiencePositions());
        cv.setExperienceDetails(dto.getExperienceDetails());
        cv.setFeedback(dto.getFeedback());
        return cv;
    }
}