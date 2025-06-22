import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { UserServiceService } from '../service/user-service.service';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {
  loginForm: FormGroup;
  errorMessage: string | null = null;
  loading: boolean = false;
  showPassword: boolean = false;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
    private userService: UserServiceService,
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

    this.authenticateUser({ username, password }).subscribe({
      next: (response) => {
        this.loading = false;
        localStorage.clear();
        localStorage.setItem('id', response.id);
        localStorage.setItem('username', response.username);
        localStorage.setItem('token', response.token);
        localStorage.setItem('userRole', response.role);
        localStorage.setItem('ChangePassword', response.ChangePassword);

        // Après authentification réussie
        const user = {
          role: response.role,
          username: response.username,
          id: response.id,
          mustChangePassword: response.mustChangePassword // ou passwordChanged: response.passwordChanged
        };
        console.log('User role is:', user.role , );
        console.log('password change', user.mustChangePassword);
        // Rediriger vers la page de connexion
        if (user.role === 'MANAGER' && user.mustChangePassword) {
          this.router.navigate(['/update-password-manager'], { queryParams: { username: user.username } });
        } else {
          this.router.navigate(['/home']);
        }
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
      // Static admin check (exemple pour SYSADMIN)
     /* if (credentials.username === 'admin' && credentials.password === 'admin123') {
        observer.next({
          token: 'fake-jwt-token', 
          role: 'SYSADMIN', 
          username: 'admin', 
          email: 'admin@actia-engineering.tn' 
        });
        observer.complete();
        return;
      }*/

      // Vérifier uniquement dans la collection users
      const url = `http://localhost:8081/users?${credentials.username.includes('@') ? 'email' : 'username'}=${credentials.username}&password=${credentials.password}`;
      this.http.get<any[]>(url).subscribe({
        next: (results) => {
          if (results.length > 0) {
            observer.next({
              token: 'fake-jwt-token',
              role: results[0].role,
              username: results[0].username,
              email: results[0].email,
              mustChangePassword: results[0].mustChangePassword,
              id: results[0].id // <-- AJOUTE CETTE LIGNE
            });
            observer.complete();
          } else {
            observer.error({ status: 401, message: 'Identifiants invalides' });
          }
        },
        error: (err) => {
          observer.error({ status: 500, message: 'Erreur serveur' });
        }
      });
    });
  }

 
}
