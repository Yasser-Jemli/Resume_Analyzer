package org.example.backend_test.Repository;

import org.example.backend_test.Entity.CvParser;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CvParserRepository extends JpaRepository<CvParser, Long> {


}
