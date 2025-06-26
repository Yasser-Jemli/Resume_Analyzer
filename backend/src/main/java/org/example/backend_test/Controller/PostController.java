package org.example.backend_test.Controller;

import org.example.backend_test.Entity.Post;
import org.example.backend_test.Entity.User;
import org.example.backend_test.Service.PostService;
import org.example.backend_test.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.example.backend_test.Entity.Role;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/posts")
public class PostController {

    @Autowired
    private PostService postService;

    @Autowired
    private UserService userService;


    @GetMapping("/getAllPosts")
    public List<Post> getAllPosts() {
        return postService.getAllPosts();
    }

    @PostMapping("/createPost/{userId}")
    public ResponseEntity<?> createPost(@PathVariable Long userId, @RequestBody Post post) {
        try {
            Optional<User> user = userService.findById(userId);
            if (user.isPresent() && user.get().getRole() == Role.MANAGER) {
                post.setUser(user.get());
                post.setCreatedAt(LocalDateTime.now());
                Post savedPost = postService.createPost(post);
                return ResponseEntity.ok(savedPost);
            } else {
                return ResponseEntity
                        .badRequest()
                        .body(Map.of("error", "User not found or not a MANAGER"));
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity
                    .badRequest()
                    .body(Map.of("error", e.getMessage()));
        }
    }


    @PutMapping("/updatePost/{id}")
    public ResponseEntity<Post> updatePost(@PathVariable Long id, @RequestBody Post postDetails) {
        return postService.updatePost(id, postDetails)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/deletPost/{id}")
    public ResponseEntity<?> deletePost(@PathVariable Long id) {
        boolean deleted = postService.deletePost(id);
        return deleted ? ResponseEntity.ok().build() : ResponseEntity.notFound().build();
    }
    @GetMapping("/manager/{userId}")
    public List<Post> getPostsByManager(@PathVariable Long userId) {
        return postService.getPostsByUserId(userId);
    }



}
