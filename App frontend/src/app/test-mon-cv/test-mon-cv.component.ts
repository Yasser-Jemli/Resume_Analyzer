import { Component } from '@angular/core';

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

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      // Vérifier si le fichier est un PDF
      if (this.selectedFile.type !== 'application/pdf') {
        this.errorMessage = 'Veuillez sélectionner un fichier PDF uniquement.';
        this.selectedFile = null;
        return;
      }
      this.errorMessage = null;
    }
  }

  uploadCV() {
    if (!this.selectedFile) return;

    // Simuler la progression de l'upload
    this.uploadProgress = 0;
    const progressInterval = setInterval(() => {
      this.uploadProgress += 10;
      if (this.uploadProgress >= 100) {
        clearInterval(progressInterval);
        this.displayPDF();
      }
    }, 200);
  }

  private displayPDF() {
    if (!this.selectedFile) return;

    const reader = new FileReader();
    reader.onload = (e: any) => {
      this.pdfSrc = e.target.result;
    };
    reader.readAsDataURL(this.selectedFile);
  }
}