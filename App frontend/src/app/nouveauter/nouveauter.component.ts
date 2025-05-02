import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface JobPost {
  title: string;
  description: string;
  skills: string[];
  budget: number;
  date_created: string;
}

@Component({
  selector: 'app-nouveauter',
  templateUrl: './nouveauter.component.html',
  styleUrls: ['./nouveauter.component.css']
})
export class NouveauterComponent implements OnInit {
  jobPosts: JobPost[] = [];
  private apiUrl = 'https://www.upwork.com/api/jobs/v1/jobs'; // Upwork API endpoint
  private apiKey = 'YOUR_UPWORK_API_KEY'; // Replace with your Upwork API key

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.getRecentJobPosts();
  }

  getRecentJobPosts() {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.apiKey}`
    });

    this.http.get<JobPost[]>(this.apiUrl, { headers }).subscribe(
      (data: any) => {
        this.jobPosts = data.jobs; // Adjust based on the API response structure
      },
      error => {
        console.error('Error fetching job posts:', error);
      }
    );
  }
}
