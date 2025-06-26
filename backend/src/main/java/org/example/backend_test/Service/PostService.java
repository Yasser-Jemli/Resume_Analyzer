package org.example.backend_test.Service;


import org.example.backend_test.Entity.Etat;
import org.example.backend_test.Entity.Post;
import org.example.backend_test.Repository.PostRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PostService {

    @Autowired
    private PostRepository postRepository;

    public List<Post> getAllPosts() {
        return postRepository.findAll();
    }

    public Optional<Post> getPostById(Long id) {
        return postRepository.findById(id);
    }

    public Post createPost(Post post) {
        return postRepository.save(post);
    }

    public Optional<Post> updatePost(Long id, Post updatedPost) {
        return postRepository.findById(id).map(post -> {
            post.setTitle(updatedPost.getTitle());
            post.setContent(updatedPost.getContent());
            post.setStatus(updatedPost.getStatus());
            post.setSkills(updatedPost.getSkills());
            return postRepository.save(post);
        });
    }

    public boolean deletePost(Long id) {
        return postRepository.findById(id).map(post -> {
            postRepository.delete(post);
            return true;
        }).orElse(false);
    }
    public List<Post> getPostsByUserId(Long userId) {
        return postRepository.findByUserId(userId);
    }


}

