import { Component, OnInit } from '@angular/core';
import { HttpEventType } from '@angular/common/http';
import { CvService } from '../services/cv.service';

export const environment = {
  production: false,
  xaiApiKey: 'your-api-key-here',
  apiUrl: 'https://your-api-url-here'
};

interface AnalysisResults {
  skills: string[];
  scores: {
    skills: number;
    experience: number;
    education: number;
  };
  recommendations: {
    missing_required: string[];
    missing_preferred: string[];
    related_skills: string[];
  };
}

interface ApiError {
  message: string;
}

@Component({
  selector: 'app-test-mon-cv',
  templateUrl: './test-mon-cv.component.html',
  styleUrls: ['./test-mon-cv.component.scss']
})
export class TestMonCvComponent implements OnInit {
  selectedFile: File | null = null;
  pdfSrc: string | ArrayBuffer | null = null;
  uploadProgress: number = 0;
  errorMessage: string = '';
  analysisResults: AnalysisResults | null = null;
  pdfisupdated: boolean = false;

  constructor(private cvService: CvService) { }

  ngOnInit(): void { }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      this.errorMessage = '';
      
      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        this.pdfSrc = e.target?.result || null;
      };
      reader.readAsArrayBuffer(file);
    } else {
      this.errorMessage = 'Please select a valid PDF file';
      this.selectedFile = null;
    }
  }

  uploadCV(): void {
    if (!this.selectedFile) {
      return;
    }

    this.cvService.uploadCV(this.selectedFile).subscribe({
      next: (event: any) => {
        if (event.type === HttpEventType.UploadProgress) {
          this.uploadProgress = Math.round(100 * (event.loaded / event.total));
        } else if (event.type === HttpEventType.Response) {
          this.analyzeCV(event.body.filename);
        }
      },
      error: (error: ApiError) => {
        this.errorMessage = 'Error uploading CV: ' + error.message;
        this.uploadProgress = 0;
      }
    });
  }

  private analyzeCV(filename: string): void {
    this.cvService.analyzeCV(filename).subscribe({
      next: (response: any) => {
        if (response.status === 'failed') {
          this.errorMessage = response.error;
          return;
        }
        this.analysisResults = response;
      },
      error: (error: ApiError) => {
        this.errorMessage = 'Error analyzing CV: ' + error.message;
      }
    });
  }
}