import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {
  loginForm: FormGroup;
  errorMessage: string | null = null;
  loading: boolean = false;
  private users: Array<{ username: string; password: string; role: string }> = [];

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
    private userService: UserService
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      rememberMe: [false]
    });
  }

  ngOnInit(): void {
    // ✅ Si l'utilisateur est déjà connecté, rediriger vers /home
    const token = localStorage.getItem('token');
    if (token) {
      this.router.navigate(['/home']);
    }

    // Initialize users here
    this.users = [
      { username: 'admin', password: 'admin123', role: 'admin' },
      { username: 'user', password: 'user123', role: 'admin' }
    ];
  }

  // Getters pratiques pour le template
  get username() {
    return this.loginForm.get('username');
  }

  get password() {
    return this.loginForm.get('password');
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.errorMessage = 'Veuillez corriger les erreurs dans le formulaire.';
      this.loginForm.markAllAsTouched();
      return;
    }

    this.errorMessage = null;
    this.loading = true;

    const { username, password, rememberMe } = this.loginForm.value;

    // Detect if username input is an email
    const isEmail = username.includes('@');
    const credentials = isEmail
      ? { email: username, password }
      : { username, password };

    console.log('🔐 Tentative de connexion :', credentials);

    this.userService.searchUser(credentials).subscribe({
      next: (response) => {
        console.log('✅ Connexion réussie :', response);
        this.loading = false;
        localStorage.clear();
        localStorage.setItem('token', response.token);
        localStorage.setItem('userRole', response.role);
        localStorage.setItem('username', response.username || username);

        if (rememberMe) {
          console.log('📝 Session persistante activée');
        }

        this.router.navigate(['/home']);
      },
      error: (error) => {
        console.error('❌ Échec de connexion :', error);
        this.errorMessage = 'Identifiants incorrects ou erreur serveur. Veuillez réessayer.';
        this.loading = false;
      }
    });
  }

  /**
   * 🔐 Simule une authentification vers un backend (remplace cette méthode par un appel réel à ton API)
   */
  private authenticateUser(credentials: { username: string; password: string }): Observable<any> {
    return new Observable((observer) => {
      const foundUser = this.users.find(
        u => u.username === credentials.username && u.password === credentials.password
      );
      if (foundUser) {
        observer.next({ token: 'fake-jwt-token', role: foundUser.role });
        observer.complete();
      } else {
        observer.error({ status: 401, message: 'Identifiants invalides' });
      }
    });
  }
}
