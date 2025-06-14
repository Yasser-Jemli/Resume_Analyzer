import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-manager-profile',
  templateUrl: './manager-profile.component.html',
  styleUrls: ['./manager-profile.component.css']
})
export class ManagerProfileComponent implements OnInit {
  username: string | null = '';
  email: string | null = '';

  constructor(private router: Router) {}

  ngOnInit(): void {
    const role = localStorage.getItem('userRole');
    if (role !== 'manager') {
      // Not a manager, redirect to home or login
      this.router.navigate(['/home']);
    }
    this.username = localStorage.getItem('username');
    this.email = localStorage.getItem('email');
  }
}
