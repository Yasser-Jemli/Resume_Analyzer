import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiUrl = 'http://localhost:8081/api/user/add'; // For add user
  private searchUrl = 'http://localhost:8081/api/user/search'; // For user search

  constructor(private http: HttpClient) { }

  addUser(user: { username: string; email: string; password: string }): Observable<any> {
    return this.http.post(this.apiUrl, user);
  }

  searchUser(credentials: { username?: string; email?: string; password: string }): Observable<any> {
    return this.http.post(this.searchUrl, credentials);
  }
  serachUserByEmail(email: string): Observable<any> {
    return this.http.post(this.searchUrl, { email });
  }
  verifyCode(data: { email: string; code: string }): Observable<any> {
    return this.http.post('http://localhost:8081/api/user/verify-code', data);

  }
  resendConfirmationCode(email: string) {
    return this.http.post('http://localhost:8081/api/user/resend-code', { email });
  }

}
