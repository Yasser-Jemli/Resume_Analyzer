import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';

interface UserByEmailResponse {
  exists: boolean;
  id?: string;
  email?: string;
  username?: string;
  role?: string;
}

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})

export class ForgotPasswordComponent {
  forgotPasswordForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private userService: UserServiceService,
    private router: Router
  ) {
    this.forgotPasswordForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  // Getter for the email form control
  get email() {
    return this.forgotPasswordForm.get('email');
  }

  onSubmit(): void {
    if (this.forgotPasswordForm.invalid) {
      return;
    }
    this.userService.getUserByEmail(this.email?.value).subscribe({
      next: (response: UserByEmailResponse) => {
        // Vérifie si la réponse contient bien un id (backend renvoie exists, id, username, email, role)
        if (response.exists) {
          // Stocker l'email et l'id dans le localStorage pour la suite du process
          localStorage.setItem('pendingForgetUser', JSON.stringify({
            id: response.id,
            email: response.email,
            username: response.username,
            role: response.role
          }));
          this.successMessage = 'A confirmation code has been sent to your email address.';

          // Appel au backend pour envoyer le code de confirmation réel
          this.userService.resendConfirmationCode(response.email!).subscribe({
            next: () => {
              // Rediriger vers la page de confirmation de code avec le mode forget
              this.router.navigate(['/confirm-code'], { queryParams: { email: response.email, mode: 'forget' } });
            },
            error: (err) => {
              this.errorMessage = 'Failed to send confirmation code.';
              this.successMessage = null;
              console.error('Resend code error:', err);
            }
          });
        } else {
          this.errorMessage = 'Email address not found.';
          this.successMessage = null;
        }
      },
      error: () => {
        this.errorMessage = 'Erreur lors de la recherche de l\'email.';
        this.successMessage = null;
      }
    });
  }
}
