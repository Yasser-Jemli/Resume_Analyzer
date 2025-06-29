import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-headers',
  templateUrl: './headers.component.html',
  styleUrls: ['./headers.component.css']
})
export class HeadersComponent {
  showMenu = false;

  constructor(private router: Router) {}

  isLoggedIn(): boolean {
    return (
      localStorage.getItem('token') !== null &&
      localStorage.getItem('username') !== null &&
      localStorage.getItem('id') !== null &&
      localStorage.getItem('role') !== null&&
      localStorage.getItem('mustChangePassword') !== null &&
      localStorage.getItem('email') !== null 
    );  
  }

  isAdmin(): boolean {
    return localStorage.getItem('username') === 'admin';
  }
  isManager(): boolean {
    return localStorage.getItem('role') === 'MANAGER';
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('id');
    localStorage.removeItem('role');
    localStorage.removeItem('mustChangePassword');
    localStorage.removeItem('email');
    //localStorage.removeItem('password');
    this.router.navigate(['/log-in']);
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }

  getUserId(): string | null {
    return localStorage.getItem('id');
  }
}