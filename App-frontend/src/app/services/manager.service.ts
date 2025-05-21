import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ManagerService {
  private apiUrl = 'http://localhost:8081/api/managers'; // Change to your backend URL

  constructor(private http: HttpClient) {}

  getManagers(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  deleteManager(email: string) {
    return this.http.post('http://localhost:8081/api/manager/delete', { email });
  }

  addManager(manager: { name: string; email: string }) {
    return this.http.post('http://localhost:8081/api/manager/add', manager);
  }
}
