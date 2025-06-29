import { Component, OnInit } from '@angular/core';
import { UserServiceService } from '../service/user-service.service';

@Component({
  selector: 'app-gestion-managers',
  templateUrl: './gestion-managers.component.html',
  styleUrls: ['./gestion-managers.component.css']
})
export class GestionManagersComponent implements OnInit {
  isAdmin: boolean = false;
  showAddForm: boolean = false;
  newManager = { username: '', email: '' };

  allUsers: any[] = [];
  filteredUsers: any[] = [];
  selectedRole: string = 'ALL';

  searchQuery: string = '';
  sortOrder: 'asc' | 'desc' = 'asc';

  showPassword: { [username: string]: boolean } = {};

  // Pagination properties
  currentPage: number = 1;
  itemsPerPage: number = 8;
  totalPages: number = 1;

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
    let users = this.allUsers;

    if (this.selectedRole !== 'ALL') {
      users = users.filter(user => user.role === this.selectedRole);
    }

    if (this.searchQuery.trim() !== '') {
      const query = this.searchQuery.toLowerCase();
      users = users.filter(user =>
        user.username.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
      );
    }

    users = users.sort((a, b) => {
      const usernameA = a.username.toLowerCase();
      const usernameB = b.username.toLowerCase();
      return this.sortOrder === 'asc'
        ? usernameA.localeCompare(usernameB)
        : usernameB.localeCompare(usernameA);
    });

    this.filteredUsers = users;
    this.currentPage = 1; // reset to first page on filter change
    this.updatePagination();
  }

  updatePagination(): void {
    if (this.filteredUsers && this.filteredUsers.length > 0) {
      this.totalPages = Math.ceil(this.filteredUsers.length / this.itemsPerPage);
    } else {
      this.totalPages = 1;
    }
  }

  get paginatedUsers(): any[] {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredUsers.slice(start, start + this.itemsPerPage);
  }

  goToPreviousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  goToNextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  toggleSortOrder(): void {
    this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    this.filterUsers();
  }

  onSearchChange(): void {
    this.filterUsers();
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
    if (!confirm(`Are you sure you want to delete ${user.username}?`)) return;

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
