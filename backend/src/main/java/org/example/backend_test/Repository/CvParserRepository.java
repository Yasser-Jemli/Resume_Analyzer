package org.example.backend_test.Repository;

import org.example.backend_test.Entity.CvParser;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CvParserRepository extends JpaRepository<CvParser, Long> {
    List<CvParser> findByUserId(Long userId);
    Optional<CvParser> findTopByUserIdOrderByCvParserIdDesc(Long userId);


}
