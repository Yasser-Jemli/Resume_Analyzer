import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { CvUploadService } from '../service/cv-upload-service.service';
import { ParserServiceService } from '../service/parser-service.service';
import { ChatInterviewServiceService } from '../service/chat-interview-service.service';
@Component({
  selector: 'app-test-mon-cv',
  templateUrl: './test-mon-cv.component.html',
  styleUrls: ['./test-mon-cv.component.css']
})
export class TestMonCvComponent implements OnInit {
  selectedFile: File | null = null;
  pdfSrc = '';
  uploadProgress = 0;
  errorMessage: string | null = null;
  pdfisupdated = false;
  customScore: any = null;
  pyresScore: any = null;
  getNoteProgress = 0;
  isGettingNote = false;
  Cv_Note: any = null;
  recommendations: string[] = [];
  skillRecommendations: any = null;
  learningPath: any = null;
  showResults = false;
  showUploadProgress = false;

  constructor(
    private cvUploadService: CvUploadService,
    private parserService: ParserServiceService,
    private userService: UserServiceService,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private chatInterviewService: ChatInterviewServiceService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input?.files?.[0];

    if (!file) {
      this.resetFileSelection('No file selected.');
      return;
    }

    if (!file.name.toLowerCase().endsWith('.pdf') || file.type !== 'application/pdf') {
      this.resetFileSelection('Please select a PDF file only.');
      return;
    }

    this.selectedFile = file;
    this.errorMessage = null;
    this.pdfSrc = '';
    this.pdfisupdated = false;
  }

  private resetFileSelection(message: string): void {
    this.selectedFile = null;
    this.pdfSrc = '';
    this.pdfisupdated = false;
    this.errorMessage = message;
  }

  startUpload(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a PDF file.';
      return;
    }

    this.uploadProgress = 0;
    this.showUploadProgress = true;
    this.errorMessage = null;
    this.cdr.detectChanges();

    this.uploadCV();
  }

  private uploadCV(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a PDF file.';
      this.showUploadProgress = false;
      return;
    }

    const metadata = {
      userid : localStorage.getItem('id') || '',
      username: localStorage.getItem('username') || '',
      usermail: localStorage.getItem('email') || '',
      postname: localStorage.getItem('postname') || '',
      postid: localStorage.getItem('postid') || ''
    };

    this.cvUploadService.uploadCV(this.selectedFile, metadata).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round((100 * event.loaded) / event.total);
          this.cdr.detectChanges();
        } else if (event.type === HttpEventType.Response) {
          this.uploadProgress = 100;
          console.log('Upload success:', event.body);
          setTimeout(() => this.displayPDF(), 500);
        }
      },
      error: (err) => {
        this.uploadProgress = 0;
        this.showUploadProgress = false;
        this.errorMessage = err.error?.message || 'Error uploading CV.';
        console.error('Upload error:', err);
        this.cdr.detectChanges();
      }
    });
  }

  private displayPDF(): void {
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
      this.resetFileSelection('Error reading PDF file.');
      this.cdr.detectChanges();
    };
    reader.readAsDataURL(this.selectedFile);
  }

  getcvnote(): void {
    this.getNoteProgress = 0;
    this.isGettingNote = true;
    this.showResults = false;

    const interval = setInterval(() => {
      if (this.getNoteProgress < 100) {
        this.getNoteProgress += 10;
        this.cdr.detectChanges();
      } else {
        clearInterval(interval);

        this.cvUploadService.getcvnote().subscribe({
          next: (cvData) => {
            console.log('CV Data:', cvData);
            if (cvData && cvData.custom) {
              this.customScore = cvData.custom;
              this.recommendations = cvData.recommendations || [];
              this.showResults = true;
            } else {
              this.errorMessage = 'No CV found for this user.';
              this.customScore = null;
              this.recommendations = [];
              this.showResults = false;
            }
            this.isGettingNote = false;
            this.cdr.detectChanges();
          },
          error: (err) => {
            this.errorMessage = 'Failed to retrieve CV data.';
            this.customScore = null;
            this.recommendations = [];
            this.isGettingNote = false;
            this.showResults = false;
            this.cdr.detectChanges();
          }
        });
      }
    }, 100);
  }

  goToChat(): void {
    // Récupérer le post depuis localStorage
    const postString = localStorage.getItem('skills');
    if (postString) {
      const post = JSON.parse(postString);
      console.log('Post a envoyer au chatbot:', post);

      this.chatInterviewService.sendposttochatbot(post).subscribe({
        next: (response) => {
          console.log('skills envoyé au chatbot:', response);
          // Rediriger vers la page de chatbot
          this.router.navigate(['/chat-bot']);
        },
        error: (error) => {
          console.error('Erreur lors de l\'envoi au chatbot:', error);
        }
      });
    } else {
      console.warn('Aucun post trouvé dans le localStorage.');
    }
    // Si le PDF n'est pas mis à jour ou que l'incrément n'est pas autorisé, naviguer directement
    this.router.navigate(['/chat-bot']);
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
