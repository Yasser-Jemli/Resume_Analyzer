package org.example.backend_test.Repository;



import org.example.backend_test.Entity.Post;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PostRepository extends JpaRepository<Post, Long> {
    List<Post> findByUserId(Long userId);
    // méthodes personnalisées si besoin
}

