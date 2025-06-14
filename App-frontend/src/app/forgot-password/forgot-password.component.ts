import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';

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
      this.errorMessage = 'Please enter a valid email address.';
      this.forgotPasswordForm.markAllAsTouched();
      return;
    }

    this.errorMessage = null;
    const email = this.forgotPasswordForm.value.email;

    this.userService.getUserByEmail(email).subscribe({
      next: (users) => {
        if (users.length > 0) {
          const user = users[0];
          // Stocker l'info utilisateur dans le localStorage pour la suite du process
          localStorage.setItem('pendingForgetUser', JSON.stringify({ id: user.id, email: user.email }));
          // Générer un code de confirmation statique ou aléatoire
          const randomCode = '123456'; // ou Math.random().toString(36).slice(-6);
          // Rediriger vers la page de confirmation de code avec le mode forget
          this.router.navigate(['/confirm-code'], { queryParams: { email, mode: 'forget', code: randomCode } });
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
