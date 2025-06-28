import { Component, OnInit } from '@angular/core';
import { PostService } from '../service/post-service.service';
import { Post } from '../models/post.model';

@Component({
  selector: 'app-mypost',
  templateUrl: './mypost.component.html',
  styleUrls: ['./mypost.component.css']
})
export class MypostComponent implements OnInit {
  posts: Post[] = [];
  status: string = 'Opened';
  newPost: Post = { title: '', content: '', skills: '', status: 'Opened' };
  editingPostId: number | null = null;
  statusOptions: string[] = ['InProgress', 'Opened', 'Terminated'];

  constructor(private postService: PostService) {}

  ngOnInit(): void {
    this.loadPosts();
  }

  loadPosts(): void {
    const userId = Number(localStorage.getItem('id'));
    if (isNaN(userId) || userId <= 0) {
      console.error('User ID not found or invalid in localStorage');
      alert('Please log in to view your posts.');
      return;
    }

      this.postService.getPostsByManager(userId).subscribe({
    next: (posts) => {
      console.log('Posts loaded:', posts);
      this.posts = posts;
    },
    error: (err) => {
      console.error('Failed to load posts:', err);
      alert('Failed to load posts: ' + err.message);
    }
  });
  }

  createPost(): void {
  const userId = Number(localStorage.getItem('id'));
  if (isNaN(userId) || userId <= 0) {
    alert('Please log in to create a post.');
    return;
  }

  if (!this.newPost.title || !this.newPost.content) {
    alert('Please fill in all required fields (title and content).');
    return;
  }

  // Ensure status defaults to 'Opened' if undefined
  if (!this.newPost.status) {
    this.newPost.status = 'Opened';
  }

  this.postService.createPost(userId, this.newPost).subscribe({
    next: (createdPost) => {
      console.log('Post created successfully:', createdPost);

      // Prepend to the posts list for immediate UI reflection
      this.posts.unshift(createdPost);

      // Reset form cleanly while preserving object structure
      this.newPost = { title: '', content: '', skills: '', status: 'Opened' };

      // Optional: Notify user
      alert('Post created successfully.');
    },
    error: (err) => {
      console.error('Error creating post:', err);
      alert('Error creating post: ' + (err.message || 'Unknown error'));
    }
  });
}


  updatePost(post: Post): void {
    if (!post.id) {
      alert('Invalid post ID.');
      return;
    }

    this.postService.updatePost(post.id, post).subscribe({
      next: () => {
        this.editingPostId = null;
        console.log('Post updated:', post);
        this.loadPosts();
      },
      error: (err) => {
        console.error('Failed to update post:', err);
        alert('Failed to update post: ' + err.message);
      }
    });
  }

  deletePost(id: number): void {
    if (!confirm('Are you sure you want to delete this post?')) return;

    this.postService.deletePost(id).subscribe({
      next: () => {
        this.posts = this.posts.filter(p => p.id !== id);
      },
      error: (err) => {
        console.error('Failed to delete post:', err);
        alert('Failed to delete post: ' + err.message);
      }
    });
  }

  editPost(post: Post): void {
    if (!post.id) {
      alert('Cannot edit post: Invalid post ID.');
      return;
    }
    this.editingPostId = post.id; // post.id is number | undefined, but checked above
  }

  cancelEdit(): void {
    this.editingPostId = null;
    this.loadPosts();
  }
}