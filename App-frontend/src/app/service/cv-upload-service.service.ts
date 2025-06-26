import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CvUploadService {
  private uploadUrl = 'http://localhost:8081/cv';
  

  constructor(private http: HttpClient) {}

  uploadCV(file: File, metadata: any): Observable<HttpEvent<any>> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', metadata.username);
    formData.append('usermail', metadata.usermail);
    formData.append('postname', metadata.postname);
    formData.append('postid', metadata.postid);

    return this.http.post(this.uploadUrl+"/upload", formData, {
      reportProgress: true,
      observe: 'events',
      responseType: 'text'
      });
  }
}