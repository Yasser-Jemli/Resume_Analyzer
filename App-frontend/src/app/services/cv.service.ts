import { Injectable } from '@angular/core';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CvService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  uploadCV(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post(`${this.apiUrl}/upload-cv`, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }

  analyzeCV(filename: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/analyze-cv`, { filename });
  }
}