package org.example.backend_test.Service;
import org.example.backend_test.Entity.CVDocument;
import org.example.backend_test.Repository.CVDocumentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CvDocumentService {

    private final CVDocumentRepository cvDocumentRepository;

    @Autowired
    public CvDocumentService(CVDocumentRepository cvDocumentRepository) {
        this.cvDocumentRepository = cvDocumentRepository;
    }

    public CVDocument save(CVDocument document) {
        return cvDocumentRepository.save(document);
    }

    public Optional<CVDocument> findById(Long id) {
        return cvDocumentRepository.findById(id);
    }

    public List<CVDocument> findAll() {
        return cvDocumentRepository.findAll();
    }

    public void deleteById(Long id) {
        cvDocumentRepository.deleteById(id);
    }

    // Add other business logic as needed
}

