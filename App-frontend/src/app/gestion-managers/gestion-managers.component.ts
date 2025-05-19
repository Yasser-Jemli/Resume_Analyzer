import { Component } from '@angular/core';

@Component({
  selector: 'app-gestion-managers',
  templateUrl: './gestion-managers.component.html',
  styleUrls: ['./gestion-managers.component.css']
})
export class GestionManagersComponent {
  isAdmin: boolean = false;

  constructor() {
    const username = localStorage.getItem('username');
    this.isAdmin = username === 'admin';
  }
}
