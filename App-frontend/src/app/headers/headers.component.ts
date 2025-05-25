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
  isManager(): void {
    const email = localStorage.getItem('email');
    // Check if the email ends with '@actia-engineering.tn'
    //return !!email && email.endsWith('@actia-engineering.tn');
  }

  logout(): void {
    localStorage.removeItem('token');
    this.router.navigate(['/log-in']);
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }
}