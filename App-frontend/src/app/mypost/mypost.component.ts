import { Component, OnInit } from '@angular/core';
import { PostService } from '../service/post-service.service';
import { Post } from '../models/post.model';


@Component({
  selector: 'app-mypost',
  templateUrl: './mypost.component.html',
  styleUrls: ['./mypost.component.css']
})
export class MypostComponent implements OnInit {
  posts: any[] = [];
  status: string = 'Opened';
  newPost: any = { title: '', content: '', author: '' , status: 'Opened' };
  editingPostId: number | null = null;
  statusOptions: string[] = ['InProgress', 'Opened', 'Terminated'];

  constructor(private postService: PostService) {}

  ngOnInit(): void {
    this.loadPosts();
  }

loadPosts(): void {
  const userId = Number(localStorage.getItem('id'));
  if (!userId) {
    console.error('User ID not found in localStorage');
    return;
  }

  this.postService.getPostsByUserId(userId).subscribe({
    next: (posts) => {
      this.posts = posts;
    },
    error: (err) => {
      console.error('Failed to load posts:', err);
    }
  });
}



  createPost(): void {
  const userId = Number(localStorage.getItem('id'));

  if (!this.newPost.title || !this.newPost.content) {
    alert('Please fill in all fields.');
    return;
  }

  this.postService.createPost(userId, {
    title: this.newPost.title,
    content: this.newPost.content,
    skills: this.newPost.skills || '',
    status: this.newPost.status || 'Opened'
  }).subscribe({
    next: (post) => {
      console.log('Post created:', post);
      this.posts.push(post);
      this.newPost = { title: '', content: '', author: '', status: 'Opened', skills: '' }; // Reset form
    },
    error: (err) => {
      const msg = err.error?.error || err.statusText || 'Unknown error';
      alert('Failed to create post: ' + msg);
    }
  });
}



  updatePost(post: any): void {
    if (!post.id) return;

    this.postService.updatePost(post.id, post).subscribe({
      next: () => {
        this.editingPostId = null;
        console.log('Post updated:', post);
        this.loadPosts();
      },
      error: (err) => {
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
        alert('Failed to delete post: ' + err.message);
      }
    });
  }

  editPost(post: any): void {
    this.editingPostId = post.id;
  }

  cancelEdit(): void {
    this.editingPostId = null;
    this.loadPosts();
  }
}
