import { Component, OnInit } from '@angular/core';
import { UserServiceService } from '../service/user-service.service';
import { ParserServiceService } from '../service/parser-service.service';
import { CvUploadService } from '../service/cv-upload-service.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  username: string | null = '';
  email: string | null = '';
  id: string | null = null;
  lastpostName: string | null = null;
  lastPosts: string | null = null;
  CV_Note: number | null = null;
  showPosts = false;
  //lastTwoPosts: string[] = [];
  lastcvName: string | null = '';
  customScore: any = null;
  fileName: string | null = null;

  showDetails = {
    detailedScores: false,
    experienceMetrics: false,
    feedback: false
  };

  constructor(
    private userService: UserServiceService,
    private parserService: ParserServiceService,
    private cvuploadService: CvUploadService
  ) {}

  ngOnInit(): void {
    this.reloadUserData();
  }

  showTab(tabName: 'detailedScores' | 'experienceMetrics' | 'feedback') {
    this.showDetails = {
      detailedScores: false,
      experienceMetrics: false,
      feedback: false
    };
    this.showDetails[tabName] = true;
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
    console.log('Reloading user data...reloadUserData');

    this.username = localStorage.getItem('username');
    this.email = localStorage.getItem('email');
    this.id = localStorage.getItem('id');
    const userId = parseInt(this.id || '0', 10);
    if (userId > 0) {
      this.cvuploadService.getAllCVInfosByUsername(this.username || '').subscribe({
        next: (cvData) => {
          console.log('CV data from backend:', cvData);
          if (cvData && cvData.length > 0) {
            const latestCV = cvData[0]; // Latest CV (assuming sorted by id DESC)
            this.lastcvName = latestCV?.fileName || 'N/A';
            this.fileName = latestCV?.fileName || 'N/A'; // Set fileName consistently
            this.lastpostName = latestCV?.postname;
          } else {
            this.lastcvName = 'N/A';
            this.lastpostName = '0';
            this.fileName = 'N/A';
          }
        },
        error: (err) => {
          console.error('Failed to fetch CV data:', err);
          this.lastcvName = 'N/A';
          this.lastpostName = '0';
          this.fileName = 'N/A';
        }
      });

      this.parserService.getCvsByUser(userId).subscribe({
        next: (data) => {
          console.log('User data from backend:', data);
          this.customScore = data.scores?.custom ?? null;
        },
        error: (err) => {
          console.error('Error fetching CVs:', err);
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