package org.example.backend_test.Controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.backend_test.Dto.CvParserRequestDto;
import org.example.backend_test.Dto.CvParserResponseDto;
import org.example.backend_test.Entity.CvParser;
import org.example.backend_test.Service.CvParserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/cv-parser")
//@CrossOrigin(origins = "*") // Allow cross-origin for frontend
public class CvParserController {

    @Autowired
    private CvParserService cvParserService;

    // POST /cv-parser/user/{userId}
    @PostMapping("/user/{userId}")
    public ResponseEntity<CvParser> uploadCv(
            @PathVariable Long userId,
            @RequestBody CvParserRequestDto dto
    ) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();

        String learningPathJson = mapper.writeValueAsString(dto.getLearning_path());
        String skillRecommendationsJson = mapper.writeValueAsString(dto.getSkill_recommendations());
        String scoresJson = mapper.writeValueAsString(dto.getScores());
        String cvnameJson = mapper.writeValueAsString(dto.getCv_name());
        String cvskills = mapper.writeValueAsString(dto.getSkills());

        CvParser savedCv = cvParserService.uploadCv(userId , learningPathJson, skillRecommendationsJson, scoresJson , cvskills);
        return ResponseEntity.ok(savedCv);
    }
    // GET /cv-parser/user/{userId}
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<CvParserResponseDto>> getCvsByUser(@PathVariable Long userId) throws JsonProcessingException {
        List<CvParser> cvList = cvParserService.getCvsByUserId(userId);
        ObjectMapper mapper = new ObjectMapper();

        List<CvParserResponseDto> responseList = cvList.stream().map(cv -> {
            try {
                return new CvParserResponseDto(
                        mapper.readValue(cv.getLearningPathJson(), Object.class),
                        mapper.readValue(cv.getSkillRecommendationsJson(), Object.class),
                        mapper.readValue(cv.getScoresJson(), Object.class),
                        mapper.readValue(cv.getSkillsJson(), Object.class)
                );
            } catch (JsonProcessingException e) {
                throw new RuntimeException("Invalid JSON in DB", e);
            }
        }).toList();

        return ResponseEntity.ok(responseList);
    }


    // GET /cv-parser/{cvId}
    @GetMapping("/{cvId}")
    public ResponseEntity<CvParserResponseDto> getCvById(@PathVariable Long cvId) throws JsonProcessingException {
        CvParser cv = cvParserService.getCvById(cvId);

        ObjectMapper mapper = new ObjectMapper();

        CvParserResponseDto responseDto = new CvParserResponseDto();
        responseDto.setLearning_path(mapper.readValue(cv.getLearningPathJson(), Object.class));
        responseDto.setSkill_recommendations(mapper.readValue(cv.getSkillRecommendationsJson(), Object.class));
        responseDto.setScores(mapper.readValue(cv.getScoresJson(), Object.class));

        return ResponseEntity.ok(responseDto);
    }


    // DELETE /cv-parser/{cvId}
    @DeleteMapping("/{cvId}")
    public ResponseEntity<Void> deleteCvById(@PathVariable Long cvId) {
        cvParserService.deleteCvById(cvId);
        return ResponseEntity.noContent().build();
    }
}

