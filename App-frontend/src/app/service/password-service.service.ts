import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PasswordServiceService {

  private apiUrl = 'http://localhost:8081/confirm-password'; // adapte l'URL à ton backend

  constructor(private http: HttpClient) { }

  // Vérifie le mot de passe auprès du backend
  confirmPassword(email: string, password: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { email, password });
  }
}
