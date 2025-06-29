package org.example.backend_test.Service;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import lombok.RequiredArgsConstructor;

import org.example.backend_test.Dto.CV_Parser_Dto;
import org.example.backend_test.Entity.CvParser;
import org.example.backend_test.Repository.CvParserRepository;
import org.example.backend_test.Repository.UserRepository;
import org.springframework.stereotype.Service;




@Service
@RequiredArgsConstructor
public class CvParserService {
    private final CvParserRepository cvParserRepository;


    public List<CvParser> getAllCvs() {
        return cvParserRepository.findAll();
    }


    public Optional<CvParser> getCvById(Long id) {
        return cvParserRepository.findById(id);
    }

    public CvParser saveCv(CvParser cv) {
        return cvParserRepository.save(cv);
    }

    public void deleteCv(Long id) {
        cvParserRepository.deleteById(id);
    }


    // Find by ID
    public CvParser findById(Long id) {
        return cvParserRepository.findByCvParserId(id)
                .orElseThrow(() -> new RuntimeException("CV not found with id: " + id));
    }

    // Find by exact skill name
    public List<CvParser> findBySkill(String skillName) {
        return cvParserRepository.findBySkillName(skillName);
    }

    // Find by multiple skills
    public List<CvParser> findBySkills(List<String> skillNames) {
        return cvParserRepository.findBySkillNames(skillNames);
    }

    // Find by skill prefix
    public List<CvParser> findBySkillPrefix(String prefix) {
        return cvParserRepository.findBySkillStartingWith(prefix);
    }

    // Get all unique skills
    public List<String> findAllUniqueSkills() {
        return cvParserRepository.findAll().stream()
                .flatMap(cv -> cv.getSkills().stream())
                .distinct()
                .sorted()
                .collect(Collectors.toList());
    }

    // Get CVs with skill statistics
    public Map<String, Long> getSkillStatistics() {
        return findAllUniqueSkills().stream()
                .collect(Collectors.toMap(
                        skill -> skill,
                        skill -> cvParserRepository.countBySkill(skill)
                ));
    }
//    public CvParser uploadCv(Long userId, String cvNameJson, String learningPathJson, String skillRecommendationsJson, String scoresJson) {
//        Optional<User> optionalUser = userRepository.findById(userId);
//        if (optionalUser.isEmpty()) {
//            throw new IllegalArgumentException("User not found with ID: " + userId);
//        }
//        User user = optionalUser.get();
//
//        // Check if the user already has a CV
//        Optional<CvParser> existingCvOpt = CvParserRepository.findTopByUserIdOrderByCvParserIdDesc(user.getId());
//
//        if (existingCvOpt.isPresent()) {
//            // Update the existing CV (replace contents)
//            CvParser cv = existingCvOpt.get();
//            cv.setCvName(cvNameJson);
//            //cv.setSkillsJson();
//            cv.setLearningPathJson(learningPathJson);
//            cv.setSkillRecommendationsJson(skillRecommendationsJson);
//            cv.setScoresJson(scoresJson);
//            return cvParserRepository.save(cv);
//        }
//
//        // Otherwise, create a new CV
//        CvParser newCv = new CvParser();
//        newCv.setUser(user);
//        newCv.setCvName(cvNameJson);
//        newCv.setLearningPathJson(learningPathJson);
//        newCv.setSkillRecommendationsJson(skillRecommendationsJson);
//        newCv.setScoresJson(scoresJson);
//        return cvParserRepository.save(newCv);
//    }
}


