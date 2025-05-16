import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  forgotPasswordForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(private fb: FormBuilder) {
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

    console.log('Password reset request submitted for email:', email);

    // Simulate a backend call
    setTimeout(() => {
      if (email === 'test@example.com') {
        this.successMessage = 'A password reset link has been sent to your email.';
        this.errorMessage = null;
      } else {
        this.errorMessage = 'Email address not found.';
        this.successMessage = null;
      }
    }, 1000); // Simulate a delay
  }
}
