import { Component, OnInit } from '@angular/core';
import { UserServiceService } from '../service/user-service.service';

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

  allUsers: any[] = [];
  filteredUsers: any[] = [];
  selectedRole: string = 'ALL';

  showPassword: { [username: string]: boolean } = {};

  constructor(private userService: UserServiceService) {
    const username = localStorage.getItem('username');
    this.isAdmin = username === 'admin';
  }

  ngOnInit(): void {
    this.loadAllUsers();
  }

  loadAllUsers(): void {
    this.userService.getAllUsers().subscribe({
      next: (data) => {
        this.allUsers = data;
        this.filterUsers();
      },
      error: (err) => console.error('Failed to load users:', err)
    });
  }

  filterUsers(): void {
    if (this.selectedRole === 'ALL') {
      this.filteredUsers = this.allUsers;
    } else {
      this.filteredUsers = this.allUsers.filter(user => user.role === this.selectedRole);
    }
  }

  toggleAddForm(): void {
    this.showAddForm = !this.showAddForm;
    this.newManager = { username: '', email: '' };
  }

  addManager(): void {
    if (!this.newManager.username || !this.newManager.email) {
      alert('Please enter both username and email.');
      return;
    }

    this.userService.checkUsernameExists(this.newManager.username).subscribe({
      next: (response) => {
        if (response.exists) {
          alert('This username is already taken.');
          return;
        }

        const email = `${this.newManager.email}@actia-engineering.tn`;
        const generatedPassword = this.generatePassword(8);

        const managerToAdd = {
          username: this.newManager.username,
          email: email,
          role: 'MANAGER',
          mustChangePassword: true,
          password: generatedPassword
        };

        this.userService.createUser(managerToAdd).subscribe({
          next: () => {
            this.toggleAddForm();
            this.loadAllUsers();
            alert(`Manager added! Password: ${generatedPassword}`);
          },
          error: (err) => alert('Failed to add manager: ' + err.message)
        });
      },
      error: (err) => alert('Error checking username: ' + err.message)
    });
  }

  deleteUser(user: any): void {
    this.userService.deleteUser(user.id).subscribe({
      next: () => this.loadAllUsers(),
      error: (err) => alert('Failed to delete user: ' + err.message)
    });
  }

  onRoleFilterChange(role: string): void {
    this.selectedRole = role;
    this.filterUsers();
  }

  togglePassword(username: string): void {
    this.showPassword[username] = !this.showPassword[username];
  }

  generatePassword(length: number = 8): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let password = '';
    for (let i = 0; i < length; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
  }


}
