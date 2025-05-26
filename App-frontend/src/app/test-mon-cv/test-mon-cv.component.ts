import { Component, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-test-mon-cv',
  templateUrl: './test-mon-cv.component.html',
  styleUrls: ['./test-mon-cv.component.css']
})
export class TestMonCvComponent {
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

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  // Handle file selection
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
      this.pdfSrc = ''; // Reset preview
      this.pdfisupdated = false;
      console.log('✅ Fichier sélectionné :', file.name);
    } else {
      this.selectedFile = null;
      this.pdfSrc = '';
      this.pdfisupdated = false;
      this.errorMessage = 'Aucun fichier sélectionné.';
    }
  }

  // Simulate file upload and display PDF
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
      console.log(`⏳ Progression : ${this.uploadProgress}%`);
      if (this.uploadProgress >= 100) {
        clearInterval(progressInterval);
        this.incrementNbrPosts();
        console.log('✅ Téléchargement terminé !');
        this.displayPDF();
        this.notifyBackendCVUpload();
      }
    }, 200);
  }

  // Display the PDF file
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
        this.cdr.detectChanges(); // Ensure Angular updates the view
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

  // Notify backend of CV upload
  private notifyBackendCVUpload(): void {
    if (!this.selectedFile) {
      console.warn('⚠️ Aucun fichier pour la notification backend');
      return;
    }

    const uploadData = {
      fileName: this.selectedFile.name,
      fileType: this.selectedFile.type,
      fileSize: this.selectedFile.size
    };

    console.log('📤 Envoi des données au backend :', uploadData);

    this.sendUploadNotification(uploadData).subscribe({
      next: (response) => {
        console.log('✅ Backend notifié avec succès:', response);
      },
      error: (error) => {
        console.error('❌ Erreur lors de la notification au backend:', error);
        this.errorMessage = 'Erreur lors de la communication avec le serveur.';
        this.cdr.detectChanges();
      }
    });

    // Always increment Nbr_Posts, regardless of backend result
    this.incrementNbrPosts();
  }

  // Send API request to backend
  private sendUploadNotification(uploadData: any): Observable<any> {
    const apiUrl = 'http://localhost:8081/api/receive_data'; // Replace with your actual backend URL
    return this.http.post(apiUrl, uploadData);
  }

  getMyNote(): void {
    this.getNoteProgress = 0;
    this.isGettingNote = true;
    const interval = setInterval(() => {
      if (this.getNoteProgress < 100) {
        this.getNoteProgress += 10;
      } else {
        clearInterval(interval);
        this.http.get<any>('http://localhost:8081/scores').subscribe({
          next: (scores) => {
            this.customScore = scores.custom;
            this.pyresScore = scores.pyres;
            this.isGettingNote = false;

            // Update all user info in the user table with pyresScore
            const email = localStorage.getItem('email');
            if (email && this.pyresScore && this.pyresScore.total_score !== undefined) {
              this.http.get<any[]>(`http://localhost:8081/users?email=${email}`).subscribe({
                next: (users) => {
                  if (users.length > 0) {
                    const user = users[0];
                    // PATCH all relevant fields
                    this.http.patch(`http://localhost:8081/users/${user.id}`, {
                      Cv_Note: this.pyresScore.total_score,
                      customScore: {
                        total_score: this.customScore.total_score,
                        detailed_scores: this.customScore.detailed_scores,
                        experience_metrics: this.customScore.experience_metrics,
                        feedback: this.customScore.feedback
                      }
                    }).subscribe({
                      next: (res) => {
                        console.log('✅ User info updated in backend:', res);
                      },
                      error: (err) => {
                        console.error('❌ Failed to update user info:', err);
                      }
                    });
                  }
                }
              });
            }
          },
          error: (err) => {
            this.errorMessage = 'Failed to fetch scores.';
            this.customScore = null;
            this.pyresScore = null;
            this.isGettingNote = false;
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

    this.http.get<any[]>(`http://localhost:8081/users?email=${email}`).subscribe({
      next: (users) => {
        if (users.length > 0) {
          const user = users[0];
          
          const newNbrPosts = (user.Nbr_Posts || 0) + 1;
          const lastcvName = this.selectedFile ? this.selectedFile.name : user.lastcvName;
          //const custom.total_score = user.Cv_Note || 0;
          console.log('User found:', user);
          this.http.patch(`http://localhost:8081/users/${user.id}`, { Nbr_Posts: newNbrPosts, lastcvName}).subscribe({
            next: (res) => {
              console.log('PATCH response:', res);
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
}