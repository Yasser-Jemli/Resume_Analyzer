import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CvUploadService {
  private uploadUrl = 'http://localhost:8081/cv/upload';

  constructor(private http: HttpClient) {}

  uploadCV(file: File, metadata: any): Observable<HttpEvent<any>> {
    const formData = new FormData();
    formData.append('file', file);
    // Send metadata as JSON string in 'data' part
    const data = {
      username: metadata.username,
      usermail: metadata.usermail,
      fileName: file.name,
      fileType: file.type,
      fileSize: file.size
    };
    formData.append('data', new Blob([JSON.stringify(data)], { type: 'application/json' }));

    return this.http.post<any>(this.uploadUrl, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }

  // Service pour récupérer les scores (utilisé dans getMyNote)
  getScores(): Observable<any> {
    return this.http.get<any>(`${this.uploadUrl}/scores`);
  }

  getLearningPath(): Observable<any> {
    return this.http.get<any>(`${this.uploadUrl}/learning_path`);
  }

  getSkillRecommendations(): Observable<any> {
    return this.http.get<any>(`${this.uploadUrl}/skill_recommendations`);
  }
}