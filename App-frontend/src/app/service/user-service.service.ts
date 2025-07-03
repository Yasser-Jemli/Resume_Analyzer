import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import {User} from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserServiceService {
  // URL de l'API pour les opérations liées aux utilisateurs
    private apiUrl = 'http://localhost:8081/auth';


  // Pour partager le username dans toute l'app
  private usernameSubject = new BehaviorSubject<string | null>(null);
  username$ = this.usernameSubject.asObservable();

  constructor(private http: HttpClient) {}

  // Authentification utilisateur (login) via POST
  login(credentials: { username?: string; email?: string; password: string }): Observable<any> {
    console.log('Login credentials:', credentials);
    return this.http.post<User>(`${this.apiUrl+'/login'}`, credentials);
  }
  
  // Récupérer un utilisateur par email
 getUserByUsername(username: string): Observable<{ exists: boolean }> {
  return this.http.get<{ exists: boolean }>(`${this.apiUrl}/check-username`, { params: { username } });
}

  // Récupérer un utilisateur par username
  
  getUserByEmail(email: string): Observable<{ exists: boolean }> {
  return this.http.get<{ exists: boolean }>(`${this.apiUrl}/check-email`, { params: { email } });
}


  // Créer un nouvel utilisateur (signup)
  createUser(user: any): Observable<any> {
    return this.http.post<User>(this.apiUrl+"/signup", user);
  }

  // Mettre à jour un utilisateur
  updateUser(id: string, data: any): Observable<any> {
    return this.http.patch<User>(`${this.apiUrl+"/updatePassword"}/${id}`, data);
  }

  // Supprimer un utilisateur
  deleteUser(id: string): Observable<any> {
  return this.http.delete<User>(`${this.apiUrl}/deleteUser/${id}`);
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
  return this.http.post<User>(`${this.apiUrl}/verify-code`, data);
}


  // Renvoyer le code de confirmation
  resendConfirmationCode(email: string): Observable<any> {
    // Corrige ici : enlève le + dans l'URL
    return this.http.post<User>(`${this.apiUrl}/resend-code`, { email });
  }

  // Récupérer tous les utilisateurs
  getAllUsers(): Observable<any[]> {
    return this.http.get<User[]>(`${this.apiUrl+"/getallusers"}`);
  }

  // Récupérer les utilisateurs par rôle (MANAGER ou CANDIDATE)
  getUsersByRole(role: string): Observable<any[]> {
    return this.http.get<User[]>(`${this.apiUrl}?role=${role}`);
  }

  // Changer la valeur de ChangePassword pour un utilisateur
  changePasswordFlag(id: string, value: boolean): Observable<any> {
    return this.http.patch<User>(`${this.apiUrl}/${id}`, { mustChangePassword: value });
  }

  // Récupérer un utilisateur par ID
  getUserById(id: string): Observable<any> {
    return this.http.get<User>(`${this.apiUrl}/${id}`);
  }

  // update Password for a user
  updatePassword(id: string, newPassword: string): Observable<any> {
   return this.http.patch(`${this.apiUrl}/updatePassword/${id}`, { newPassword });
 }

  // Récupérer le mot de passe d'un utilisateur par son id
  getPassword(id: string): Observable<any> {
    return this.http.get<User>(`${this.apiUrl}/getPassword/${id}`);
  }
   checkUsernameExists(username: string): Observable<{ exists: boolean }> {
    return this.http.get<{ exists: boolean }>(`${this.apiUrl}/check-username?username=${username}`);
  }
  sendCode(email: string): Observable<any> {
  //console.log("Sending confirmation code to:", email);
  return this.http.post(`${this.apiUrl}/send-login-code`, { email });
}

  getCVbyuserID(userId: number): Observable<Blob> {
  return this.http.get(`/cv-parser/user/${userId}/download`, { responseType: 'blob' });
   }
}
