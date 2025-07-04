import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserServiceService } from '../service/user-service.service';
import { Router } from '@angular/router';

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
  loading: boolean = false;  // <--- Loading flag

  constructor(
    private fb: FormBuilder,
    private userService: UserServiceService,
    private router: Router
  ) {
    this.forgotPasswordForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  get email() {
    return this.forgotPasswordForm.get('email');
  }

  onSubmit(): void {
    if (this.loading) return;  // Prevent multiple submits
    if (this.forgotPasswordForm.invalid) {
      this.errorMessage = 'Please enter a valid email.';
      return;
    }

    this.loading = true;           // Start loading
    this.errorMessage = null;
    this.successMessage = null;

    this.userService.getUserByEmail(this.email?.value).subscribe({
      next: (response: UserByEmailResponse) => {
        console.log('Email search response:', response);
        if (response.exists) {
          const emailToUse = response.email || this.email?.value;
          localStorage.setItem('pendingForgetUser', JSON.stringify({
            id: response.id,
            email: emailToUse,
            username: response.username,
            role: response.role
          }));

          console.log('Resending code to:', emailToUse);

          this.userService.resendConfirmationCode(emailToUse).subscribe({
            next: (res: any) => {
              this.loading = false;
              this.successMessage = res.message || 'A confirmation code has been sent to your email address.';
              this.router.navigate(['/confirm-code'], { queryParams: { email: emailToUse, mode: 'forget' } });
            },
            error: (err) => {
              this.loading = false;
              this.errorMessage = 'Failed to send confirmation code.';
              console.error('Resend code error:', err);
            }
          });
        } else {
          console.log('response', response); // <-- Affiche aussi ici si besoin
          this.loading = false;
          this.errorMessage = 'Email address not found.';
        }
      },
      error: (err) => {
        this.loading = false;
        console.log('response', err); // <-- Affiche l'erreur ici
        this.errorMessage = 'Error searching for email.';
      }
    });
  }
}
