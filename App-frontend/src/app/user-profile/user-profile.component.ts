import { Component, OnInit } from '@angular/core';
import { UserServiceService } from '../service/user-service.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  username: string | null = '';
  email: string | null = '';
  id: string | null = null;
  Nbr_Posts: number | null = null;
  lastPosts: string | null = null;
  CV_Note: number | null = null;
  showPosts = false;
  lastTwoPosts: string[] = [];
  lastcvName: string | null = '';
  customScore: any = null;

  showDetails = {
    detailedScores: false,
    experienceMetrics: false,
    feedback: false
  };

  constructor(private userService: UserServiceService) {}

  ngOnInit(): void {
    this.username = localStorage.getItem('username');
    this.email = localStorage.getItem('email');
    this.id = localStorage.getItem('id'); 
    this.Nbr_Posts = Number(localStorage.getItem('Nbr_Posts')) || 0;
    this.lastPosts = localStorage.getItem('lastPosts');
    this.lastcvName = localStorage.getItem('lastcvName') || '';
    this.customScore = JSON.parse(localStorage.getItem('customScore') || '{}') || { total_score: 0 };
    if (this.username) {
      this.userService.getUserByUsername(this.username).subscribe({
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

    if (this.username) {
      this.userService.getUserByUsername(this.username).subscribe({
        next: (users) => {
          if (users.length > 0) {
            const user = users[0];
            if (user.password === password) {
              if (confirm('Are you sure you want to delete your profile? This action cannot be undone.')) {
                this.userService.deleteUser(user.id).subscribe({
                  next: () => {
                    alert('Profile deleted successfully.');
                    localStorage.clear();
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
  }

  getBadgeClass(score: number): string {
    if (score < 50) {
      return 'bg-danger text-light';
    } else if (score < 70) {
      return 'bg-warning text-dark';
    } else {
      return 'bg-success text-light';
    }
  }

  reloadUserData() {
    if (this.username) {
      this.userService.getUserByUsername(this.username).subscribe({
        next: (users) => {
          if (users.length > 0) {
            console.log('Reloaded user data:', users);
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

  updatePassword(): void {
    const oldPassword = prompt('Entrez votre mot de passe actuel :');
    if (!oldPassword) {
      alert('Changement annulé.');
      return;
    }

    const newPassword = prompt('Entrez le nouveau mot de passe (min 6 caractères) :');
    if (!newPassword || newPassword.length < 6) {
      alert('Le nouveau mot de passe doit contenir au moins 6 caractères.');
      return;
    }

    if (this.username) {
      const userId = localStorage.getItem('id');
      if (!userId) {
        alert('Utilisateur introuvable.');
        return;
      }

      // Utilisation du service getPassword
      this.userService.getPassword(userId).subscribe({
        next: (response) => {
          const storedPassword = response.password;
          if (storedPassword !== oldPassword) {
            alert('Mot de passe actuel incorrect.');
            return;
          }
          this.userService.updatePassword(userId, newPassword).subscribe({
            next: () => {
              alert('Mot de passe mis à jour avec succès.');
            },
            error: (err) => {
              alert('Erreur lors de la mise à jour du mot de passe.');
              console.error('Update error:', err);
            }
          });
        },
        error: (err) => {
          alert('Erreur lors de la récupération du mot de passe.');
          console.error('Get password error:', err);
        }
      });
    }
  }
}
