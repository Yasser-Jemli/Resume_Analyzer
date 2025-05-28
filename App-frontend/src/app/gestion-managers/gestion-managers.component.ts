import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-gestion-managers',
  templateUrl: './gestion-managers.component.html',
  styleUrls: ['./gestion-managers.component.css']
})
export class GestionManagersComponent implements OnInit {
  isAdmin: boolean = false;
  managers: any[] = [];
  showAddForm: boolean = false;
  newManager = { username: '', email: '' };

  constructor(private http: HttpClient) {
    const username = localStorage.getItem('username');
    this.isAdmin = username === 'admin';
  }

  ngOnInit(): void {
    this.loadManagers();
  }

  loadManagers() {
    this.http.get<any[]>('http://localhost:8081/managers').subscribe({
      next: (data) => this.managers = data,
      error: (err) => console.error('Failed to load managers:', err)
    });
  }

  toggleAddForm() {
    this.showAddForm = !this.showAddForm;
    this.newManager = { username: '', email: '' };
  }

  addManager() {
    if (!this.newManager.username || !this.newManager.email) {
      alert('Please enter both username and email.');
      return;
    }

    // Générer un mot de passe aléatoire de 8 caractères
    const randomPassword = Math.random().toString(36).slice(-8);

    // Always append the fixed domain
    const email = `${this.newManager.email}@actia-engineering.tn`;

    const managerToAdd = {
      username: this.newManager.username,
      password: randomPassword,
      email: email,
      role: 'manager' 
    };

    this.http.post('http://localhost:8081/managers', managerToAdd).subscribe({
      next: () => {
        this.toggleAddForm();
        this.loadManagers();
        alert(`Manager added! Password: ${randomPassword}`);
      },
      error: (err) => alert('Failed to add manager: ' + err.message)
    });
  }

  deleteManager(manager: any) {
    this.http.delete(`http://localhost:8081/managers/${manager.id}`).subscribe({
      next: () => this.loadManagers(),
      error: (err) => alert('Failed to delete manager: ' + err.message)
    });
  }
}
