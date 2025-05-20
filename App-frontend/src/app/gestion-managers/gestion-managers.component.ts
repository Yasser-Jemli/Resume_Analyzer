import { Component, OnInit } from '@angular/core';
import { ManagerService } from '../services/manager.service';

@Component({
  selector: 'app-gestion-managers',
  templateUrl: './gestion-managers.component.html',
  styleUrls: ['./gestion-managers.component.css']
})
export class GestionManagersComponent implements OnInit {
  isAdmin: boolean = false;
  showAddForm: boolean = false;
  newManager = { name: '', email: '' };
  //managers: any[] = [];
   managers = [
    { name: 'chakhari imed', email: 'chakhariimed@actia-engineering.tn' },
    { name: 'aziz bouslimi', email: 'azizbousslimi@actia-engineering.tn' }
  ];

  constructor(private managerService: ManagerService) {
    const username = localStorage.getItem('username');
    this.isAdmin = username === 'admin';
  }

  ngOnInit() {
    this.loadManagers();
  }

  loadManagers() {
    this.managerService.getManagers().subscribe(data => {
      this.managers = data;
    });
  }

  deleteManager(index: number) {
    const manager = this.managers[index];
    // Assuming each manager has an 'id' property
    this.managerService.deleteManager(manager.email).subscribe({
      next: () => {
        this.loadManagers(); // Refresh the list after deletion
      },
      error: (err) => {
        console.error('Failed to delete manager:', err);
      }
    });
  }

  toggleAddForm() {
    this.showAddForm = !this.showAddForm;
    this.newManager = { name: '', email: '' };
  }

  addManager() {
    if (this.newManager.name && this.newManager.email) {
      this.managerService.addManager(this.newManager).subscribe({
        next: () => {
          this.loadManagers(); // Refresh the list after adding
          this.toggleAddForm();
        },
        error: (err) => {
          console.error('Failed to add manager:', err);
        }
      });
    }
  }
}
