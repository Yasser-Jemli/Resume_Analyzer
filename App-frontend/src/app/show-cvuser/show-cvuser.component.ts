import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-show-cvuser',
  templateUrl: './show-cvuser.component.html',
  styleUrls: ['./show-cvuser.component.css']
})
export class ShowCvuserComponent implements OnInit {
  users: any[] = [];

  constructor(private http: HttpClient) {}

ngOnInit(): void {
  this.http.get<any[]>('http://localhost:8081/users').subscribe({
    next: (data) => {
      this.users = data.sort((a, b) => {
        const scoreA = a.customScore?.total_score ?? a.CV_Note ?? 0;
        const scoreB = b.customScore?.total_score ?? b.CV_Note ?? 0;
        return scoreB - scoreA; // Descending order
      });
    },
    error: (err) => console.error('Failed to load users:', err)
  });
  }
}
