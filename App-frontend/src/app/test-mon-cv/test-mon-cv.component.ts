import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { CvUploadService } from '../service/cv-upload-service.service';
import { Parser } from 'html2canvas/dist/types/css/syntax/parser';
import { ParserServiceService } from '../service/parser-service.service';

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

  showUploadProgress = false;  // <-- Nouvelle variable pour afficher la barre

  constructor(
    private cvUploadService: CvUploadService,
    private parserService: ParserServiceService,
    private userService: UserServiceService,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
   /* this.fetchLearningPath();
    this.fetchSkillRecommendations();**/
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input?.files?.[0];

    if (!file) {
      this.resetFileSelection('Aucun fichier sélectionné.');
      return;
    }

    if (!file.name.toLowerCase().endsWith('.pdf') || file.type !== 'application/pdf') {
      this.resetFileSelection('Veuillez sélectionner un fichier PDF uniquement.');
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

  // Nouvelle méthode appelée par le bouton pour commencer l'upload
  startUpload(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Veuillez sélectionner un fichier PDF.';
      return;
    }
    this.uploadProgress = 0;
    this.showUploadProgress = true;  // Afficher la barre tout de suite
    this.errorMessage = null;

    this.cdr.detectChanges();  // Forcer le rafraîchissement avant upload

    this.uploadCV();
  }

  // uploadCV fait uniquement l'appel réel
  private uploadCV(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Veuillez sélectionner un fichier PDF.';
      this.showUploadProgress = false;
      return;
    }

    const metadata = {
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
          //this.showUploadProgress = false;  // Cacher la barre quand upload fini
          this.cdr.detectChanges();
          console.log('Upload success:', event.body);
          setTimeout(() => this.displayPDF(), 500);
        }
      },
      error: (err) => {
        this.uploadProgress = 0;
        //this.showUploadProgress = false;
        this.errorMessage = err.error?.message || 'Erreur lors du téléchargement du CV.';
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
      this.resetFileSelection('Erreur lors de la lecture du fichier PDF.');
      this.cdr.detectChanges();
    };
    reader.readAsDataURL(this.selectedFile);
  }

getMyNote(): void {
  this.getNoteProgress = 0;
  this.isGettingNote = true;
  this.showResults = false;

  const interval = setInterval(() => {
    if (this.getNoteProgress < 100) {
      this.getNoteProgress += 10;
      this.cdr.detectChanges();
    } else {
      clearInterval(interval);

      
     const userId: number = parseInt(localStorage.getItem('id') || '0', 10);


      this.parserService.getCvsByUser(userId).subscribe({
        next: (cvList) => {
          if (cvList.length > 0) {
            const latestCv = cvList[cvList.length - 1]; // or sort by date if available

            console.log('Latest CV:', latestCv);

            this.customScore = latestCv.scores?.custom || null;
            this.recommendations = latestCv.skill_recommendations || [];

            this.showResults = true;
          } else {
            this.errorMessage = 'Aucun CV trouvé pour cet utilisateur.';
            this.customScore = null;
            this.recommendations = [];
            this.showResults = false;
          }

          this.isGettingNote = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          this.errorMessage = 'Échec de récupération des données CV.';
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

          const currentNbrPosts = parseInt(localStorage.getItem('Nbr_Posts') || '0', 10);
          const newNbrPosts = currentNbrPosts + 1;
          const lastcvName = this.selectedFile?.name || '';

          this.userService.updateUser(userId, {
            Nbr_Posts: newNbrPosts,
            lastcvName
          }).subscribe();
        }
      },
      error: (err) => console.error('Failed to fetch user:', err)
    });
  }

/*  private fetchLearningPath(): void {
    this.parserService.getLearningPath().subscribe({
      next: (data) => {
        this.learningPath = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erreur récupération learning path:', err);
        this.learningPath = null;
      }
    });
  }

  private fetchSkillRecommendations(): void {
    this.parserService.getSkillRecommendations().subscribe({
      next: (data) => {
        this.skillRecommendations = data.recommendations;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erreur récupération recommandations:', err);
        this.skillRecommendations = null;
      }
    });
  }*/

  getBadgeClass(score: number): string {
    if (score < 50) return 'bg-danger text-light';
    if (score < 70) return 'bg-warning text-dark';
    return 'bg-success text-light';
  }

  getKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }
}
