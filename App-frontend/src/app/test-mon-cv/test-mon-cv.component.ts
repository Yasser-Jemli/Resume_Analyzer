import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';
import { HttpClient } from '@angular/common/http';
import { CvUploadService } from '../service/cv-upload-service.service';
import { HttpEventType } from '@angular/common/http';
// Install via: npm install file-saver

@Component({
  selector: 'app-test-mon-cv',
  templateUrl: './test-mon-cv.component.html',
  styleUrls: ['./test-mon-cv.component.css']
})
export class TestMonCvComponent implements OnInit {
  selectedFile: File | null = null;
  pdfSrc: string = '';
  uploadProgress = 0;
  errorMessage: string | null = null;
  pdfisupdated: boolean = false;
  customScore: any = null;
  pyresScore: any = null;
  getNoteProgress = 0;
  isGettingNote = false;
  Cv_Note: any = null;
  recommendations: string[] = [];
  skillRecommendations: any = null;
  learningPath: any = null;
  showResults: boolean = false;

  constructor(
    private parserService: CvUploadService,
    private userService: UserServiceService,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.fetchLearningPath();
    this.fetchSkillRecommendations();
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (!file.name.toLowerCase().endsWith('.pdf') || file.type !== 'application/pdf') {
        this.errorMessage = 'Veuillez sélectionner un fichier PDF uniquement.';
        this.selectedFile = null;
        this.pdfSrc = '';
        this.pdfisupdated = false;
        return;
      }
      this.selectedFile = file;
      this.errorMessage = null;
      this.pdfSrc = '';
      this.pdfisupdated = false;
    } else {
      this.selectedFile = null;
      this.pdfSrc = '';
      this.pdfisupdated = false;
      this.errorMessage = 'Aucun fichier sélectionné.';
    }
  }

  uploadCV() {
    if (!this.selectedFile) {
      this.errorMessage = 'Veuillez sélectionner un fichier PDF.';
      return;
    }
    this.uploadProgress = 0;
    this.errorMessage = null;
    this.notifyBackendCVUpload();
  }

  private displayPDF() {
    if (!this.selectedFile) return;
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      if (e.target?.result) {
        this.pdfSrc = e.target.result as string;
        this.pdfisupdated = true;
        this.cdr.detectChanges();
      }
    };
    reader.onerror = () => {
      this.errorMessage = 'Erreur lors de la lecture du fichier PDF.';
      this.pdfisupdated = false;
      this.pdfSrc = '';
      this.cdr.detectChanges();
    };
    reader.readAsDataURL(this.selectedFile);
  }

  private notifyBackendCVUpload(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Aucun fichier sélectionné.';
      return;
    }
    const uploadData = {
      username: localStorage.getItem('username'),
      usermail: localStorage.getItem('email')
    };
    if (!uploadData.username || !uploadData.usermail) {
      this.errorMessage = 'Informations utilisateur manquantes (username ou email).';
      return;
    }
    console.log('Sending upload data:', uploadData);
    this.parserService.uploadCV(this.selectedFile, uploadData).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round((100 * event.loaded) / event.total);
        } else if (event.type === HttpEventType.Response) {
          console.log('Upload successful:', event.body);
          this.errorMessage = null;
          this.displayPDF();
        }
      },
      error: (err) => {
        this.uploadProgress = 0;
        this.errorMessage = err.error?.message || 'Erreur lors du téléchargement du CV.';
        console.error('Upload error:', JSON.stringify(err, null, 2));
      }
    });
  }

  getMyNote(): void {
    this.getNoteProgress = 0;
    this.isGettingNote = true;
    this.showResults = false;
    const interval = setInterval(() => {
      if (this.getNoteProgress < 100) {
        this.getNoteProgress += 10;
      } else {
        clearInterval(interval);
        this.parserService.getScores().subscribe({
          next: (scores) => {
            this.customScore = scores.custom;
            this.recommendations = scores.recommendations || [];
            this.showResults = true;
            const email = localStorage.getItem('email');
            if (
              email &&
              this.customScore &&
              this.customScore.total_score !== undefined &&
              this.customScore.detailed_scores &&
              this.customScore.experience_metrics
            ) {
              this.userService.getUserByEmail(email).subscribe({
                next: (response) => {
                  if (response.exists) {
                    const userId = localStorage.getItem('id');
                    if (!userId) return;
                    const lastcvName = this.selectedFile ? this.selectedFile.name : '';
                    const lastPosts = localStorage.getItem('postName') || '';
                    this.userService.updateUser(userId, {
                      Cv_Note: this.pyresScore ? this.pyresScore.total_score : null,
                      customScore: {
                        total_score: this.customScore.total_score,
                        detailed_scores: this.customScore.detailed_scores,
                        experience_metrics: this.customScore.experience_metrics,
                        feedback: this.customScore.feedback
                      },
                      lastcvName,
                      lastPosts
                    }).subscribe();
                  }
                },
                error: (err) => {
                  console.error('Failed to fetch user for score update:', err);
                }
              });
            }
          },
          error: (err) => {
            this.errorMessage = 'Failed to fetch scores.';
            this.customScore = null;
            this.isGettingNote = false;
            this.recommendations = [];
            this.showResults = false;
          }
        });
      }
    }, 100);
  }

  goToChat(): void {
    if (this.pdfisupdated && localStorage.getItem('canIncrementCV') === 'true') {
      this.incrementNbrPosts();
      localStorage.removeItem('canIncrementCV');
    }
    this.router.navigate(['/chat-bot']);
  }

  private incrementNbrPosts(): void {
    const email = localStorage.getItem('email');
    if (!email) return;
    this.userService.getUserByEmail(email).subscribe({
      next: (response) => {
        if (response.exists) {
          const userId = localStorage.getItem('id');
          if (!userId) return;
          const newNbrPosts = ((localStorage.getItem('Nbr_Posts') as any) || 0) + 1;
          const lastcvName = this.selectedFile ? this.selectedFile.name : '';
          this.userService.updateUser(userId, { Nbr_Posts: newNbrPosts, lastcvName }).subscribe();
        }
      },
      error: (err) => {
        console.error('Failed to fetch user:', err);
      }
    });
  }

  fetchLearningPath() {
    this.parserService.getLearningPath().subscribe({
      next: (data) => {
        this.learningPath = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Failed to fetch learning path:', err);
        this.learningPath = null;
      }
    });
  }

  fetchSkillRecommendations() {
    this.parserService.getSkillRecommendations().subscribe({
      next: (data) => {
        this.skillRecommendations = data.recommendations;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Failed to fetch skill recommendations:', err);
        this.skillRecommendations = null;
      }
    });
  }

  getBadgeClass(score: number): string {
    if (score < 50) return 'bg-danger text-light';
    if (score < 70) return 'bg-warning text-dark';
    return 'bg-success text-light';
  }

  getKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }
}