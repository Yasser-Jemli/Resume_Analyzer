import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ManagerServiceService {
  private apiUrl = 'http://localhost:8081/managers';

  constructor(private http: HttpClient) {}

  // Récupérer tous les managers
  getAllManagers(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  // Récupérer un manager par email
  getManagerByEmail(email: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?email=${email}`);
  }

  // Ajouter un manager
  addManager(manager: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, manager);
  }

  // Supprimer un manager
  deleteManager(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
  getManagerByUsername(username: string): Observable<any[]> {
  return this.http.get<any[]>(`http://localhost:8081/managers?username=${username}`);
}
getUserByUsername(username: string): Observable<any[]> {
  return this.http.get<any[]>(`http://localhost:8081/users?username=${username}`);
}
}
