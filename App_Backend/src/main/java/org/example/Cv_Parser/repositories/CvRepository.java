package org.example.Cv_Parser.repositories;

import org.example.Cv_Parser.models.Cv;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CvRepository extends JpaRepository<Cv, Long> {
}
