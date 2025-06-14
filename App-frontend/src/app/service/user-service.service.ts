import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserServiceService {
  private apiUrl = 'http://localhost:8081/users';

  // Pour partager le username dans toute l'app
  private usernameSubject = new BehaviorSubject<string | null>(null);
  username$ = this.usernameSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Authentification utilisateur (login)
  login(username: string, password: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?username=${username}&password=${password}`);
  }

  // Récupérer un utilisateur par email
  getUserByEmail(email: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?email=${email}`);
  }

  // Récupérer un utilisateur par username
  getUserByUsername(username: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?username=${username}`);
  }

  // Créer un nouvel utilisateur (signup)
  createUser(user: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, user);
  }

  // Mettre à jour un utilisateur
  updateUser(id: string, data: any): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}/${id}`, data);
  }

  // Supprimer un utilisateur
  deleteUser(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }

  // Gestion du username partagé
  setUsername(username: string): void {
    this.usernameSubject.next(username);
  }

  clearUsername(): void {
    this.usernameSubject.next(null);
  }

  // Vérifier le code de confirmation
  verifyCode(data: { email: string; code: string }): Observable<any> {
    // À adapter selon ton backend, ici exemple avec /verify-code
    return this.http.post<any>('http://localhost:8081/verify-code', data);
  }

  // Renvoyer le code de confirmation
  resendConfirmationCode(email: string): Observable<any> {
    // À adapter selon ton backend, ici exemple avec /resend-code
    return this.http.post<any>('http://localhost:8081/resend-code', { email });
  }
  getManagerByUsername(username: string): Observable<any[]> {
  return this.http.get<any[]>(`http://localhost:8081/managers?username=${username}`);
}
}
