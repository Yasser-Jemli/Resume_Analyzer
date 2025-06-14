import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  username: string | null = '';
  email: string | null = '';
  id: number | null = null;
  Nbr_Posts: number | null = null;
  lastPosts: string | null = null;
  CV_Note: number | null = null;
  showPosts = false;
  lastTwoPosts: string[] = [];
  lastcvName: string | null = '';
  customScore: any = null;

  // New: visibility toggles for score sections
  showDetails = {
    detailedScores: false,
    experienceMetrics: false,
    feedback: false
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.username = localStorage.getItem('username');
    if (this.username) {
      this.http.get<any[]>(`http://localhost:8081/users?username=${this.username}`).subscribe({
        next: (users) => {
          if (users.length > 0) {
            const user = users[0];
            this.email = user.email;
            this.id = user.id;
            this.username = user.username;
            this.Nbr_Posts = user.Nbr_Posts || 0;
            this.lastPosts = user.lastPosts || null;
            this.customScore = user.customScore || { total_score: 0 };
            this.lastcvName = user.lastcvName || '';
          }
        },
        error: (err) => {
          // handle error
        }
      });
    }
  }
  showTab(tabName: 'detailedScores' | 'experienceMetrics' | 'feedback') {
  this.showDetails = {
    detailedScores: false,
    experienceMetrics: false,
    feedback: false
  };
  this.showDetails[tabName] = true;
}


  deleteMyProfile(): void {
    const password = prompt('Please enter your password to confirm profile deletion:');
    if (!password) {
      alert('Profile deletion cancelled.');
      return;
    }

    this.http.get<any[]>(`http://localhost:8081/users?username=${this.username}`).subscribe({
      next: (users) => {
        if (users.length > 0) {
          const user = users[0];
          if (user.password === password) {
            if (confirm('Are you sure you want to delete your profile? This action cannot be undone.')) {
              // Suppression du profil
              this.http.delete(`http://localhost:8081/users/${user.id}`).subscribe({
                next: () => {
                  alert('Profile deleted successfully.');
                  localStorage.clear();
                  // Appel logout (redirige vers /log-in)
                  window.location.href = '/log-in';
                },
                error: (err) => {
                  alert('Failed to delete profile.');
                  console.error('Delete error:', err);
                }
              });
            }
          } else {
            alert('Incorrect password. Profile not deleted.');
          }
        } else {
          alert('User not found.');
        }
      },
      error: (err) => {
        alert('Error verifying password.');
        console.error('Fetch user error:', err);
      }
    });
  }
  getBadgeClass(score: number): string {
  if (score < 50) {
    return 'bg-danger text-light'; // Rouge
  } else if (score < 70) {
    return 'bg-warning text-dark'; // Jaune
  } else {
    return 'bg-success text-light'; // Vert
  }
}

reloadUserData() {
  if (this.username) {
    this.http.get<any[]>(`http://localhost:8081/users?username=${this.username}`).subscribe({
      next: (users) => {
        if (users.length > 0) {
          const user = users[0];
          this.email = user.email;
          this.id = user.id;
          this.username = user.username;
          this.Nbr_Posts = user.Nbr_Posts || 0;
          this.lastPosts = user.lastPosts || null;
          this.customScore = user.customScore || { total_score: 0 };
          this.lastcvName = user.lastcvName || '';
        }
      }
    });
  }
}

}
