package org.example.backend_test.Repository;

import org.example.backend_test.Entity.CvParser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface CvParserRepository extends JpaRepository<CvParser, Long> {
    // Find by ID
    Optional<CvParser> findByCvParserId(Long id);

    // Find by skill name
    @Query("SELECT c FROM CvParser c JOIN c.skills s WHERE s = :skillName")
    List<CvParser> findBySkillName(@Param("skillName") String skillName);

    // Find by multiple skills
    @Query("SELECT c FROM CvParser c JOIN c.skills s WHERE s IN :skillNames")
    List<CvParser> findBySkillNames(@Param("skillNames") List<String> skillNames);

    // Find by skill prefix
    @Query("SELECT DISTINCT c FROM CvParser c JOIN c.skills s WHERE s LIKE CONCAT(:prefix, '%')")
    List<CvParser> findBySkillStartingWith(@Param("prefix") String prefix);

    // Count by skill
    @Query("SELECT COUNT(c) FROM CvParser c JOIN c.skills s WHERE s = :skillName")
    Long countBySkill(@Param("skillName") String skillName);

}
