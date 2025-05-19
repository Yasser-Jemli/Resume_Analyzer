import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {
  loginForm: FormGroup;
  errorMessage: string | null = null;
  loading: boolean = false;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router
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

    console.log('🔐 Tentative de connexion :', { username, rememberMe });

    this.authenticateUser({ username, password }).subscribe({
      next: (response) => {
        console.log('✅ Connexion réussie :', response);
        this.loading = false;
        localStorage.clear();
        // ✅ Stockage du token et du rôle
        localStorage.setItem('token', response.token);
        localStorage.setItem('userRole', response.role);
        localStorage.setItem('username', username); // Add this line

        if (rememberMe) {
          // Exemple : stocker dans localStorage pour persistance (déjà fait ci-dessus)
          console.log('📝 Session persistante activée');
        }

        // Rediriger vers la page d'accueil
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
      const users = [
        { username: 'admin', password: 'admin123', role: 'admin' },
        { username: 'user', password: 'user123', role: 'admin' }
      ];

      setTimeout(() => {
        const foundUser = users.find(
          u => u.username === credentials.username && u.password === credentials.password
        );
        if (foundUser) {
          observer.next({ token: 'fake-jwt-token', role: foundUser.role });
          observer.complete();
        } else {
          observer.error({ status: 401, message: 'Identifiants invalides' });
        }
      }, 1000);
    });
  }
}
