import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router'; // <-- Add this import

interface JiraIssue {
  key: string;
  fields: {
    summary: string;
    description: string;
    customfield_10056?: string; // responsibilities
    customfield_10057?: string; // skills
    customfield_10055?: string; // description
  };
}

@Component({
  selector: 'app-nouveauter',
  templateUrl: './nouveauter.component.html',
  styleUrls: ['./nouveauter.component.css']
})
export class NouveauterComponent implements OnInit {
  issues: JiraIssue[] = [];
  skillsList: string[] = [];
  // Update the URL to your running json-server endpoint
  private apiUrl = 'http://localhost:8081/issues';

  constructor(private http: HttpClient, private router: Router) {} // <-- Inject Router

  ngOnInit() {
    this.http.get<JiraIssue[]>(this.apiUrl).subscribe(
      data => {
        this.issues = data;
        console.log('Issues:', this.issues); // Check what you get
      },
      error => {
        console.error('Error fetching issues from json-server:', error);
      }
    );
  }

  goToTestMonCV() {
    this.router.navigate(['/test-mon-cv']);
  }
}







