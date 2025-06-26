package org.example.backend_test.Repository;

import org.example.backend_test.Entity.CVDocument;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CVDocumentRepository extends JpaRepository<CVDocument, Long> {
}
