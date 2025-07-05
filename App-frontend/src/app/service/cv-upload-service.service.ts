import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

// Interface for CV metadata
export interface CVInfo {
  id: number;
  fileName: string;
  fileType: string;
  username: string;
  usermail: string;
  postname: string;
  postid: string;
}

// Interface for CV upload metadata
export interface CVUploadMetadata {
  username: string;
  usermail: string;
  postname: string;
  postid: string;
}

@Injectable({
  providedIn: 'root'
})
export class CvUploadService {
  private readonly uploadUrl = 'http://localhost:8081/cv';
  private readonly uploadParser = 'http://localhost:8000/cv';

  constructor(private http: HttpClient) {}

  /**
   * Uploads a CV file with metadata to the backend.
   * @param file The CV file to upload.
   * @param metadata The metadata for the CV (username, usermail, postname, postid).
   * @returns Observable<HttpEvent<string>> for tracking upload progress and response.
   */
  uploadCV(file: File, metadata: CVUploadMetadata): Observable<HttpEvent<string>> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', metadata.username);
    formData.append('usermail', metadata.usermail);
    formData.append('postname', metadata.postname);
    formData.append('postid', metadata.postid);

    return this.http.post(`${this.uploadUrl}/upload`, formData, {
      reportProgress: true,
      observe: 'events',
      responseType: 'text'
    }).pipe(
      catchError((error) => {
        console.error('CV upload failed:', error);
        return throwError(() => new Error('Failed to upload CV: ' + (error.message || 'Unknown error')));
      })
    );
  }

  /**
   * Uploads a CV file with metadata to the backend.
   * @param file The CV file to upload.
   * @param metadata The metadata for the CV (username, usermail, postname, postid).
   * @returns Observable<HttpEvent<string>> for tracking upload progress and response.
   */
  uploadCVParser(file: File, metadata: CVUploadMetadata): Observable<HttpEvent<string>> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', metadata.username);
    formData.append('usermail', metadata.usermail);
    formData.append('postname', metadata.postname);
    formData.append('postid', metadata.postid);

    return this.http.post(`${this.uploadParser}/upload`, formData, {
      reportProgress: true,
      observe: 'events',
      responseType: 'text'
    }).pipe(
      catchError((error) => {
        console.error('CV upload failed:', error);
        return throwError(() => new Error('Failed to upload CV: ' + (error.message || 'Unknown error')));
      })
    );
  }

  /**
   * Downloads a CV file for the given username.
   * @param username The username whose CV to download.
   * @returns Observable<Blob> containing the CV file.
   */
  downloadCV(username: string): Observable<Blob> {
    return this.http.get(`${this.uploadUrl}/download/${username}`, { responseType: 'blob' }).pipe(
      catchError((error) => {
        console.error('CV download failed:', error);
        return throwError(() => new Error('Failed to download CV: ' + (error.message || 'Unknown error')));
      })
    );
  }

  /**
   * Retrieves metadata for all CVs associated with the given username.
   * @param username The username to fetch CV metadata for.
   * @returns Observable<CVInfo[]> containing the list of CV metadata.
   */
  getAllCVInfosByUsername(username: string): Observable<CVInfo[]> {
    return this.http.get<CVInfo[]>(`${this.uploadUrl}/listcv/${username}`).pipe(
      catchError((error) => {
        console.error('Failed to fetch CV metadata:', error);
        return throwError(() => new Error('Failed to fetch CV metadata: ' + (error.message || 'Unknown error')));
      })
    );
  }

  /**
   * Retrieves a CV file and its filename for the given username.
   * @param username The username whose CV to retrieve.
   * @returns Observable<{ blob: Blob; fileName: string }> containing the CV file and filename.
   */
  getCVByUsername(username: string): Observable<{ blob: Blob; fileName: string }> {
    return this.http.get(`${this.uploadUrl}/getcv/${username}`, {
      responseType: 'blob',
      observe: 'response'
    }).pipe(
      map((response: HttpResponse<Blob>) => {
        const contentDisposition = response.headers.get('Content-Disposition') || '';
        let fileName = 'CV.pdf';
        const matches = /filename="([^"]+)"/.exec(contentDisposition);
        if (matches && matches[1]) {
          fileName = matches[1];
        }
        if (!response.body) {
          throw new Error('No CV file data received');
        }
        return { blob: response.body, fileName };
      }),
      catchError((error) => {
        console.error('Failed to retrieve CV:', error);
        return throwError(() => new Error('Failed to retrieve CV: ' + (error.message || 'Unknown error')));
      })
    );
  }
  getAllCVs(): Observable<CVInfo[]> {
  return this.http.get<CVInfo[]>(`${this.uploadUrl}/all`).pipe(
    catchError((error) => {
      console.error('Failed to fetch all CVs:', error);
      return throwError(() => new Error('Failed to fetch all CVs: ' + (error.message || 'Unknown error')));
    })
  );
  }
  getcvnote(): Observable<any> {
    return this.http.get<any>(`${this.uploadUrl}/scores`).pipe(
      catchError((error) => {
        console.error('Failed to fetch CV note:', error);
        return throwError(() => new Error('Failed to fetch CV note: ' + (error.message || 'Unknown error')));
      })
    );
  }
  getCandidateCVsForManagerPosts(): Observable<any[]> {
    return this.http.get<any[]>(`${this.uploadUrl}/candidate-cvs`);
  }
}