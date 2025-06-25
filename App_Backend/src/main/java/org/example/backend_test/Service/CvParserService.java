package org.example.backend_test.Service;

import org.example.backend_test.Entity.CvParser;
import org.example.backend_test.Entity.User;
import org.example.backend_test.Repository.CvParserRepository;
import org.example.backend_test.Repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CvParserService {

    @Autowired
    private CvParserRepository cvParserRepository;

    @Autowired
    private UserRepository userRepository;

    // Save a new CV for a user
    public CvParser saveCv(Long userId, String cvname, String learningPathJson, String skillRecommendationsJson, String scoresJson) {
        Optional<User> optionalUser = userRepository.findById(userId);

        if (optionalUser.isEmpty()) {
            throw new IllegalArgumentException("User not found with ID: " + userId);
        }

        User user = optionalUser.get();

        CvParser cv = new CvParser();
        cv.setUser(user);
        cv.setCvName(cvname);
        cv.setLearningPathJson(learningPathJson);
        cv.setSkillRecommendationsJson(skillRecommendationsJson);
        cv.setScoresJson(scoresJson);

        return cvParserRepository.save(cv);
    }

    // Get a CV by its ID
    public CvParser getCvById(Long cvId) {
        return cvParserRepository.findById(cvId)
                .orElseThrow(() -> new IllegalArgumentException("CV not found with ID: " + cvId));
    }

    // Get all CVs for a specific user
    public List<CvParser> getCvsByUserId(Long userId) {
        return cvParserRepository.findByUserId(userId);
    }

    // Delete a CV by its ID
    public void deleteCvById(Long cvId) {
        if (!cvParserRepository.existsById(cvId)) {
            throw new IllegalArgumentException("CV not found with ID: " + cvId);
        }
        cvParserRepository.deleteById(cvId);
    }
    public CvParser uploadCv(Long userId, String cvNameJson, String learningPathJson, String skillRecommendationsJson, String scoresJson) {
        Optional<User> optionalUser = userRepository.findById(userId);
        if (optionalUser.isEmpty()) {
            throw new IllegalArgumentException("User not found with ID: " + userId);
        }

        User user = optionalUser.get();

        // Check if the user already has a CV
        Optional<CvParser> existingCvOpt = cvParserRepository.findTopByUserIdOrderByCvParserIdDesc(user.getId());

        if (existingCvOpt.isPresent()) {
            // Update the existing CV (replace contents)
            CvParser cv = existingCvOpt.get();
            cv.setCvName(cvNameJson);
            //cv.setSkillsJson();
            cv.setLearningPathJson(learningPathJson);
            cv.setSkillRecommendationsJson(skillRecommendationsJson);
            cv.setScoresJson(scoresJson);
            return cvParserRepository.save(cv);
        }

        // Otherwise, create a new CV
        CvParser newCv = new CvParser();
        newCv.setUser(user);
        newCv.setCvName(cvNameJson);
        newCv.setLearningPathJson(learningPathJson);
        newCv.setSkillRecommendationsJson(skillRecommendationsJson);
        newCv.setScoresJson(scoresJson);
        return cvParserRepository.save(newCv);
    }


}
