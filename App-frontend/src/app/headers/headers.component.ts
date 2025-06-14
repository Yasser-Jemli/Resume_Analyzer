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
    return localStorage.getItem('token') !== null;
  }

  isAdmin(): boolean {
    return localStorage.getItem('username') === 'admin';
  }
  isManager(): boolean {
    return localStorage.getItem('userRole') === 'manager';
  }

  logout(): void {
    localStorage.removeItem('token');
    this.router.navigate(['/log-in']);
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }
}