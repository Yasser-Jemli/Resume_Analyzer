import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserServiceService } from '../service/user-service.service';
import { CvUploadService } from '../service/cv-upload-service.service';

@Component({
  selector: 'app-show-cvuser',
  templateUrl: './show-cvuser.component.html',
  styleUrls: ['./show-cvuser.component.css']
})
export class ShowCvuserComponent implements OnInit {
  candidateUsers: any[] = [];
  loadingDownload: boolean = false; // optional loader flag for download

  constructor(
    private http: HttpClient,
    private userService: UserServiceService,
    private cvuploadService:CvUploadService
  ) {}

  ngOnInit(): void {
    console.log('Component initialized, fetching users...');
    this.loadCandidateUsers();
  }

  loadCandidateUsers(): void {
    this.cvuploadService.getAllCVs().subscribe({
      next: (data) => {
        this.candidateUsers = data;
        console.log('Users loaded:', this.candidateUsers);
        this.candidateUsers.forEach(user => {
          user.lastcvName = user.lastcvName || `${user.username}_CV.pdf`;//||user.submittedPostName = user.submittedPostName; // Fallback name if lastcvName is not set
          user.submittedPostName = user.postname || 'N/A';
        });
        console.log('Candidate users loaded:', this.candidateUsers);
      },
      error: (err) => console.error('Failed to load users:', err)
    });
  }

downloadCV(user: any): void {
  this.loadingDownload = true;

  const fallbackFileName = user.lastcvName || `${user.username}_CV.pdf`;

  this.cvuploadService.downloadCV(user.username).subscribe({
    next: (blob) => {
      const blobUrl = window.URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = fallbackFileName;
      document.body.appendChild(link); // Ensure Safari compatibility
      link.click();
      document.body.removeChild(link);

      window.URL.revokeObjectURL(blobUrl);

      console.log(`✅ CV downloaded for user: ${user.username}`);
      this.loadingDownload = false;
    },
    error: (err) => {
      console.error(`❌ Failed to download CV for user ${user.username}:`, err);
      this.loadingDownload = false;
      alert(`Failed to download CV for ${user.username}. Please try again.`);
    }
  });
}

}
