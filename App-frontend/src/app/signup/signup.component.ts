import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  signupForm: FormGroup;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.signupForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
  }

  // Custom validator to check if password and confirmPassword match
  private passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { mismatch: true };
  }

  // Getters for form controls
  get username() {
    return this.signupForm.get('username');
  }

  get email() {
    return this.signupForm.get('email');
  }

  get password() {
    return this.signupForm.get('password');
  }

  get confirmPassword() {
    return this.signupForm.get('confirmPassword');
  }

  onSubmit(): void {
    if (this.signupForm.invalid) {
      this.errorMessage = 'Please correct the errors in the form.';
      this.signupForm.markAllAsTouched();
      return;
    }

    this.errorMessage = null;
    const { username, email, password } = this.signupForm.value;

    // Send data to json-server to add user
    const apiUrl = 'http://localhost:8081/users'; // json-server users endpoint
    const signupData = { username, email, password };

    this.http.post(apiUrl, signupData).subscribe({
      next: (response) => {
        console.log('Signup successful:', response);
        this.successMessage = 'Signup successful! Please log in.';
        this.errorMessage = null;
        this.signupForm.reset();
      },
      error: (error) => {
        console.error('Signup failed:', error);
        this.errorMessage = 'Signup failed. Please try again.';
        this.successMessage = null;
      }
    });
  }
}
