import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';

@Component({
  selector: 'app-update-password',
  templateUrl: './update-password.component.html',
  styleUrls: ['./update-password.component.css']
})
export class UpdatePasswordComponent implements OnInit {
  updatePasswordForm: FormGroup;
  successMessage: string | null = null;
  errorMessage: string | null = null;
  email: string = '';
  code: string = '';
  userId: string = '';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private userService: UserServiceService,
    private router: Router
  ) {
    this.updatePasswordForm = this.fb.group({
      newPassword: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.email = params['email'] || '';
      this.code = params['code'] || '';
      this.userId = params['id'] || '';
    });
  }

  get newPassword() {
    return this.updatePasswordForm.get('newPassword');
  }

  onSubmit(): void {
    if (this.updatePasswordForm.invalid) {
      this.errorMessage = 'Please enter a valid password.';
      this.updatePasswordForm.markAllAsTouched();
      return;
    }

    const newPassword = this.updatePasswordForm.value.newPassword;
    console.log('Attempting to update password for:', this.email, 'New password:', newPassword);

    // Utilise l'id pour mettre à jour l'utilisateur
    this.userService.updatePassword(this.userId, newPassword).subscribe({
      next: (res) => {
        console.log('Password update response:', res);
        this.successMessage = 'Password updated successfully!';
        this.errorMessage = null;
        localStorage.removeItem('pendingForgetUser');
        setTimeout(() => this.router.navigate(['/log-in']), 1500);
      },
      error: (err) => {
        console.error('Failed to update password:', err);
        this.errorMessage = 'Failed to update password.';
        this.successMessage = null;
      }
    });
  }
}