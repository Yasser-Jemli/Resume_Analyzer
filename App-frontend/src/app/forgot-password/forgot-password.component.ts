import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../services/user.service'; // Import UserService
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  forgotPasswordForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router) {
    this.forgotPasswordForm = this.fb.group({
      email: ['test@example.com', [Validators.required, Validators.email]] // email statique pour test
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

    // Log the email sent to the backend
    console.log('🔎 Email sent to backend for password reset:', email);

    // Use the UserService to check if the email exists
    this.userService.serachUserByEmail(email).subscribe({
      next: (response) => {
        this.successMessage = 'A code for changing your password has been sent to your email.';
        this.errorMessage = null;
        console.log('Password reset code sent to:', email);
      },
      error: (error) => {
        this.errorMessage = 'Email address not found.';
    // Chercher l'email dans le json-server
    this.http.get<any[]>(`http://localhost:8081/users?email=${email}`).subscribe({
      next: (users) => {
        if (users.length > 0) {
          // Générer un mot de passe aléatoire de 6 caractères
          const randomPassword = Math.random().toString(36).slice(-6);
          // Rediriger vers la page de mise à jour du mot de passe avec l'email en paramètre
          this.router.navigate(['/update-password'], { queryParams: { email, code: randomPassword } });
        } else {
          this.errorMessage = 'Email address not found.';
          this.successMessage = null;
        }
      },
      error: () => {
        this.errorMessage = 'Erreur lors de la recherche de l\'email.';
        this.successMessage = null;
        console.error('Email not found:', error);
      }
    });
  }
}
