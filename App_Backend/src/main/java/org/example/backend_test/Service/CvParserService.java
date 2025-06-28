package org.example.backend_test.Service;

import java.util.List;
import java.util.Optional;

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


