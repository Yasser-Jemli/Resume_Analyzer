import { Component, OnInit } from '@angular/core';
import { ManagerServiceService } from '../service/manager-service.service';

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

  constructor(private managerService: ManagerServiceService) {
    const username = localStorage.getItem('username');
    this.isAdmin = username === 'admin';
  }

  ngOnInit(): void {
    this.loadManagers();
  }

  loadManagers() {
    this.managerService.getAllManagers().subscribe({
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

  // Vérifier si le username existe déjà chez les managers
  this.managerService.getManagerByUsername(this.newManager.username).subscribe({
    next: (managers) => {
      if (managers.length > 0) {
        alert('This username is already taken.');
        return;
      }

      // Vérifier si le username existe déjà chez les users
      this.managerService.getUserByUsername(this.newManager.username).subscribe({
        next: (users) => {
          if (users.length > 0) {
            alert('This username is already taken.');
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

          this.managerService.addManager(managerToAdd).subscribe({
            next: () => {
              this.toggleAddForm();
              this.loadManagers();
              alert(`Manager added! Password: ${randomPassword}`);
            },
            error: (err) => alert('Failed to add manager: ' + err.message)
          });
        },
        error: (err) => alert('Error checking username in users: ' + err.message)
      });
    },
    error: (err) => alert('Error checking username in managers: ' + err.message)
  });
}

  deleteManager(manager: any) {
    this.managerService.deleteManager(manager.id).subscribe({
      next: () => this.loadManagers(),
      error: (err) => alert('Failed to delete manager: ' + err.message)
    });
  }
}
