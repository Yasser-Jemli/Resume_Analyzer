import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ParserServiceService {
  private apiUrl = 'http://localhost:8081/cv-parser';
  private apiUrl2 = 'http://localhost:8081/cv/scores';

  constructor(private http: HttpClient) {}

  // POST: Upload a CV for a specific user
  uploadCv(userId: number, data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/user/${userId}`, data);
  }

  // GET: Fetch all CVs for a specific user
  getCvsByUser(ueserid : number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl2}`);
  }

  // GET: Fetch a specific CV by its ID
  getCvById(cvId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${cvId}`);
  }

  // DELETE: Delete a specific CV by its ID
  deleteCvById(cvId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${cvId}`);
  }
}
