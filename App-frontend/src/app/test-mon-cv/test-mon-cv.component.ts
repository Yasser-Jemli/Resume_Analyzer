// test-mon-cv.component.ts
import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { CvUploadService } from '../service/cv-upload-service.service';
import { ParserServiceService } from '../service/parser-service.service';
import { UserServiceService } from '../service/user-service.service';
import { ChatInterviewServiceService } from '../service/chat-interview-service.service';

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
  pdfisupdated = false;

  customScore: number | null = null;
  skillsScore: number | null = null;
  experienceScore: number | null = null;
  educationScore: number | null = null;
  feedback: string[] = [];
  recommendations: string[] = [];

  isGettingNote = false;
  getNoteProgress = 0;
  showResults = false;
  showUploadProgress = false;

  lastUploadResponse: any = null; // Add this property to store the last upload response
  isCvUploaded: boolean = false;

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
      this.resetFileSelection('Please select a valid PDF file.');
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
      userid: localStorage.getItem('id') || '',
      username: localStorage.getItem('username') || '',
      usermail: localStorage.getItem('email') || '',
      postname: localStorage.getItem('postname') || '',
      postid: localStorage.getItem('postid') || ''
    };

    this.cvUploadService.uploadCVParser(this.selectedFile, metadata).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round((100 * event.loaded) / event.total);
          this.cdr.detectChanges();
        } else if (event.type === HttpEventType.Response) {
          const responseBody = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
          this.lastUploadResponse = responseBody; // Store the response for later
          setTimeout(() => this.displayPDF(), 300);
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

    this.cvUploadService.uploadCV(this.selectedFile, metadata).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round((100 * event.loaded) / event.total);
          this.cdr.detectChanges();
        } else if (event.type === HttpEventType.Response) {
          const responseBody = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
          this.lastUploadResponse = responseBody;
          this.isCvUploaded = true; // Enable the button
          setTimeout(() => this.displayPDF(), 300);
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
            if (cvData?.scores?.custom) {
              const custom = cvData.scores.custom;
              this.customScore = custom.total_score ?? null;
              this.skillsScore = custom.detailed_scores?.skills ?? null;
              this.experienceScore = custom.detailed_scores?.experience ?? null;
              this.educationScore = custom.detailed_scores?.education ?? null;
              this.feedback = custom.feedback ?? [];
              this.recommendations = cvData.skill_recommendations?.recommendations || [];
              this.showResults = true;
              this.errorMessage = null;
            } else {
              this.clearScores();
              this.errorMessage = 'No scores found in the response.';
            }
            this.isGettingNote = false;
            this.cdr.detectChanges();
          },
          error: (err) => {
            this.errorMessage = 'Failed to retrieve CV data.';
            this.clearScores();
            this.isGettingNote = false;
            this.cdr.detectChanges();
          }
        });
      }
    }, 100);
  }

  goToChat(): void {
    const postString = localStorage.getItem('skills');
    if (postString) {
      const post = JSON.parse(postString);
      console.log('Post sent to chatbot:', post);
      this.chatInterviewService.sendposttochatbot(post).subscribe({
        next: () => this.router.navigate(['/chat-bot']),
        error: (error) => {
          console.error('Error sending to chatbot:', error);
          this.router.navigate(['/chat-bot']);
        }
      });
    } else {
      console.warn('No post found in localStorage.');
      this.router.navigate(['/chat-bot']);
    }
  }

  getBadgeClass(score: number): string {
    if (score < 50) return 'bg-danger text-light';
    if (score < 70) return 'bg-warning text-dark';
    return 'bg-success text-light';
  }

  getKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }

  private parseScoresFromResponse(data: any): void {
    if (data && data.scores && data.scores.custom) {
      const custom = data.scores.custom;
      this.customScore = custom.total_score ?? null;
      this.skillsScore = custom.detailed_scores?.skills ?? null;
      this.experienceScore = custom.detailed_scores?.experience ?? null;
      this.educationScore = custom.detailed_scores?.education ?? null;
      this.feedback = custom.feedback ?? [];
      this.showResults = true;
      this.errorMessage = null;
    } else {
      this.clearScores();
      this.errorMessage = 'No scores found in the response.';
    }
    this.cdr.detectChanges();
  }

  private clearScores(): void {
    this.customScore = null;
    this.skillsScore = null;
    this.experienceScore = null;
    this.educationScore = null;
    this.feedback = [];
    this.showResults = false;
  }

  // Call this when the user clicks "Get My Note"
  showScoresFromLastUpload(): void {
    if (this.lastUploadResponse) {
      this.parseScoresFromResponse(this.lastUploadResponse);
    } else {
      this.errorMessage = 'No CV data available. Please upload a CV first.';
      this.showResults = false;
    }
  }
}
