import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PostService } from '../service/post-service.service';
import { ChatInterviewServiceService } from '../service/chat-interview-service.service';
import { Post } from '../models/post.model'; // Use shared model

@Component({
  selector: 'app-nouveauter',
  templateUrl: './nouveauter.component.html',
  styleUrls: ['./nouveauter.component.css']
})
export class NouveauterComponent implements OnInit {
  posts: Post[] = [];
  filteredPosts: Post[] = [];

  constructor(
    private postService: PostService,
    private chatInterviewService: ChatInterviewServiceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.postService.getPosts().subscribe({
      next: (data: Post[]) => {
        this.posts = data;

        // ✅ Only include posts with status 'Opened' or 'InProgress'
        this.filteredPosts = this.posts.filter(
          post => post.status === 'Opened' || post.status === 'InProgress'
        );

        console.log('Filtered Posts:', this.filteredPosts);
      },
      error: (err) => {
        console.error('Failed to load posts:', err);
      }
    });
  }

  goToTestMonCV(post: Post): void {
    // Optional: use a real field like post.skills instead of content
    const skills = post.content?.split(',').map(s => s.trim()) || [];

    localStorage.setItem('postSkills', JSON.stringify(skills));
    localStorage.setItem('postName', post.title);

    this.chatInterviewService.setSkills(skills);
    this.router.navigate(['/test-mon-cv']);
  }

  onSubmit(): void {
    localStorage.setItem('canIncrementCV', 'true');
  }
}
