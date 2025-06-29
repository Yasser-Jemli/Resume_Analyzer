package org.example.Cv_Parser.services;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.example.Cv_Parser.models.Cv;
import org.example.Cv_Parser.repositories.CvRepository;
import org.springframework.stereotype.Service;




@Service
@RequiredArgsConstructor
public class CvService {
    private final CvRepository cvRepository;

    public List<Cv> getAllCvs() {
        return cvRepository.findAll();
    }

    public Cv getCvById(Long id) {
        return cvRepository.findById(id).orElse(null);
    }

    public Cv saveCv(Cv cv) {
        return cvRepository.save(cv);
    }

    public void deleteCv(Long id) {
        cvRepository.deleteById(id);
    }
}
