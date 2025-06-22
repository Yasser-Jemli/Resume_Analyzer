import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';
// Import services
import { ParserServiceService } from '../service/parser-service.service';
import { UserServiceService } from '../service/user-service.service';
import { HttpClient } from '@angular/common/http';

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
    private parserService: ParserServiceService,
    private userService: UserServiceService,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private http: HttpClient // Only for upload notification, can be refactored too
  ) {}

  getBadgeClass(score: number): string {
    if (score < 50) {
      return 'bg-danger text-light';
    } else if (score < 70) {
      return 'bg-warning text-dark';
    } else {
      return 'bg-success text-light';
    }
  }

  goToChat(): void {
    if (this.pdfisupdated && localStorage.getItem('canIncrementCV') === 'true') {
      this.incrementNbrPosts();
      localStorage.removeItem('canIncrementCV');
      console.log('Nbr_Posts incremented and flag removed');
    }
    this.router.navigate(['/chat-bot']);
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (file.type !== 'application/pdf') {
        this.errorMessage = 'Veuillez sélectionner un fichier PDF uniquement.';
        this.selectedFile = null;
        this.pdfSrc = '';
        this.pdfisupdated = false;
        console.warn('❌ Fichier non PDF sélectionné');
        return;
      }
      this.selectedFile = file;
      this.errorMessage = null;
      this.pdfSrc = '';
      this.pdfisupdated = false;
      console.log('✅ Fichier sélectionné :', file.name);
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
      console.warn('⚠️ Aucun fichier sélectionné');
      return;
    }
    this.uploadProgress = 0;
    this.errorMessage = null;
    const progressInterval = setInterval(() => {
      this.uploadProgress += 10;
      if (this.uploadProgress >= 100) {
        clearInterval(progressInterval);
        console.log('✅ Téléchargement terminé !');
        this.displayPDF();
        this.notifyBackendCVUpload();
      }
    }, 200);
  }

  private displayPDF() {
    if (!this.selectedFile) {
      this.errorMessage = 'Aucun fichier sélectionné pour l\'aperçu.';
      console.warn('⚠️ Aucun fichier pour l\'aperçu');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      if (e.target?.result) {
        this.pdfSrc = e.target.result as string;
        this.pdfisupdated = true;
        this.cdr.detectChanges();
        console.log('📄 PDF affiché avec succès');
      } else {
        this.errorMessage = 'Erreur lors de la lecture du fichier PDF.';
        this.pdfisupdated = false;
        console.error('❌ Résultat de FileReader vide');
      }
    };
    reader.onerror = () => {
      this.errorMessage = 'Erreur lors de la lecture du fichier PDF.';
      this.pdfisupdated = false;
      this.pdfSrc = '';
      console.error('❌ Erreur de lecture du fichier PDF');
      this.cdr.detectChanges();
    };
    reader.readAsDataURL(this.selectedFile);
  }

  private notifyBackendCVUpload(): void {
    if (!this.selectedFile) {
      console.warn('⚠️ Aucun fichier pour la notification backend');
      return;
    }
    const uploadData = {
      username: localStorage.getItem('username'),
      usermail: localStorage.getItem('email'),
      //filepath: this.selectedFile.name,
      fileName: this.selectedFile.name,
      fileType: this.selectedFile.type,
      fileSize: this.selectedFile.size
    };
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

            // Ajout de la mise à jour du score utilisateur
            const email = localStorage.getItem('email');
            if (
              email &&
              this.customScore &&
              this.customScore.total_score !== undefined &&
              this.customScore.detailed_scores &&
              this.customScore.experience_metrics
            ) {
              // Utilisation du service utilisateur ici
              this.userService.getUserByEmail(email).subscribe({
                next: (users) => {
                  if (users.length > 0) {
                    const user = users[0];
                    const lastcvName = this.selectedFile ? this.selectedFile.name : user.lastcvName;
                    const lastPosts = localStorage.getItem('postName') || user.lastPosts;
                    this.userService.updateUser(user.id, {
                      Cv_Note: this.pyresScore ? this.pyresScore.total_score : null,
                      customScore: {
                        total_score: this.customScore.total_score,
                        detailed_scores: this.customScore.detailed_scores,
                        experience_metrics: this.customScore.experience_metrics,
                        feedback: this.customScore.feedback
                      },
                      lastcvName,
                      lastPosts
                    }).subscribe({
                      next: () => {
                        console.log('✅ User scores, CV name, and endtwoPosts updated in backend');
                      },
                      error: (err) => {
                        console.error('❌ Failed to update user scores, CV name, or endtwoPosts:', err);
                      }
                    });
                  }
                },
                error: (err) => {
                  console.error('❌ Failed to fetch user for score update:', err);
                }
              });
            } else {
              console.warn('customScore or its properties are null:', this.customScore);
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

  private incrementNbrPosts(): void {
    const email = localStorage.getItem('email');
    if (!email) {
      console.warn('No email in localStorage');
      return;
    }
    this.userService.getUserByEmail(email).subscribe({
      next: (users) => {
        if (users.length > 0) {
          const user = users[0];
          const newNbrPosts = (user.Nbr_Posts || 0) + 1;
          const lastcvName = this.selectedFile ? this.selectedFile.name : user.lastcvName;
          this.userService.updateUser(user.id, { Nbr_Posts: newNbrPosts, lastcvName }).subscribe({
            next: (res) => {
              console.log('✅ Nbr_Posts incremented:', newNbrPosts);
              console.log('✅ lastcvName updated:', lastcvName);
            },
            error: (err) => {
              console.error('❌ Failed to update Nbr_Posts or lastcvName:', err);
            }
          });
        } else {
          console.warn('No user found with email:', email);
        }
      },
      error: (err) => {
        console.error('❌ Failed to fetch user:', err);
      }
    });
  }

  ngOnInit() {
    this.fetchLearningPath();
    this.fetchSkillRecommendations();
  }

  fetchLearningPath() {
    this.parserService.getLearningPath().subscribe({
      next: (data) => {
        this.learningPath = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('❌ Failed to fetch learning path:', err);
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
        console.error('❌ Failed to fetch skill recommendations:', err);
        this.skillRecommendations = null;
      }
    });
  }

  getKeys(obj: any): string[] {
    return obj ? Object.keys(obj) : [];
  }
}