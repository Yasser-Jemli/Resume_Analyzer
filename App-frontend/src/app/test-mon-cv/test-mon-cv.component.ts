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
  }

  // Send API request to backend
  private sendUploadNotification(uploadData: any): Observable<any> {
    const apiUrl = 'http://localhost:8081/api/receive_data'; // Replace with your actual backend URL
    return this.http.post(apiUrl, uploadData);
  }

  getMyNote(): void {
    console.log('📄 Get My Note button clicked!');
    // TODO: Implement logic to fetch or calculate the note for the uploaded CV and send to yasser jemli 
  }
}