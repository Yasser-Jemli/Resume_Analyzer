import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PostService } from '../service/post-service.service';
import { ChatInterviewServiceService } from '../service/chat-interview-service.service';
import { Post } from '../models/post.model';

@Component({
  selector: 'app-nouveauter',
  templateUrl: './nouveauter.component.html',
  styleUrls: ['./nouveauter.component.css']
})
export class NouveauterComponent implements OnInit {
  posts: Post[] = [];
  filteredPosts: Post[] = [];
  selectedPost: Post | null = null;

  constructor(
    private postService: PostService,
    private chatInterviewService: ChatInterviewServiceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.postService.getPosts().subscribe({
      next: (data: Post[]) => {
        this.posts = data;

        // Only include posts with status 'Opened' or 'InProgress'
        this.filteredPosts = this.posts.filter(
          post => post.status === 'Opened' || post.status === 'InProgress'
        );

        // Save all post IDs to localStorage
        //localStorage.setItem('postsid', JSON.stringify(this.filteredPosts.map(post => post.id)));
      },
      error: (err) => {
        console.error('Failed to load posts:', err);
      }
    });
  }

  selectPost(post: Post): void {
    this.selectedPost = post;
  }

  onSubmit(): void {
    if (!this.selectedPost) {
      alert('Please select a post before submitting.');
      return;
    }
  
    localStorage.setItem('postname', this.selectedPost.title);
    const postId = this.selectedPost?.id?.toString() ?? '';
    localStorage.setItem('postid', postId);



    console.log('Stored in localStorage:', {
      postname: this.selectedPost.title,
      postid: this.selectedPost.id
    });

    // Optional: Navigate or trigger something else
    this.chatInterviewService.setSkills(
      this.selectedPost.content?.split(',').map(s => s.trim()) || []
    );
    this.router.navigate(['/test-mon-cv']);
  }
}
