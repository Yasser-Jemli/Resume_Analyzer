import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../services/user.service'; // Import UserService

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  forgotPasswordForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(private fb: FormBuilder, private userService: UserService) {
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
        this.successMessage = null;
        console.error('Email not found:', error);
      }
    });
  }
}
