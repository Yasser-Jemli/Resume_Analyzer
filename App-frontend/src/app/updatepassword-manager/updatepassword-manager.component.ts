import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-updatepassword-manager',
  templateUrl: './updatepassword-manager.component.html',
  styleUrls: ['./updatepassword-manager.component.css']
})
export class UpdatepasswordManagerComponent {
  username: string = '';
  passwordForm: FormGroup;
  loading = false;
  errorMessage = '';
  successMessage = '';
  showPassword = false;

  constructor(
    private route: ActivatedRoute,
    private userService: UserServiceService,
    private router: Router,
    private fb: FormBuilder
  ) {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'];
    });

    this.passwordForm = this.fb.group({
      newPassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordsMatchValidator });
  }

  get newPassword() {
    return this.passwordForm.get('newPassword');
  }

  get confirmPassword() {
    return this.passwordForm.get('confirmPassword');
  }

  passwordsMatchValidator(form: FormGroup) {
    const password = form.get('newPassword')?.value;
    const confirm = form.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }

  onSubmit() {
    this.errorMessage = '';
    this.successMessage = '';
    if (this.passwordForm.invalid) return;

    this.loading = true;
    const userId = localStorage.getItem('id');
    if (!userId) {
      this.errorMessage = 'Utilisateur non authentifié.';
      this.loading = false;
      return;
    }

    this.userService.updatePassword(userId, this.newPassword?.value).subscribe({
      next: () => {
        this.successMessage = 'Mot de passe mis à jour avec succès !';
        this.loading = false;

        // Récupère le rôle depuis le localStorage
        const role = localStorage.getItem('role');
        setTimeout(() => {
          if (role === 'MANAGER') {
            this.router.navigate(['/manager-profile', userId]);
          } else if (role === 'CANDIDATE') {
            this.router.navigate(['/profile', userId]);
          } else if (role === 'SYSADMIN' || role === 'ADMIN') {
            this.router.navigate(['/gestion-managers']);
          } else {
            this.router.navigate(['/home']);
          }
        }, 1500);
      },
      error: () => {
        this.errorMessage = 'Erreur lors de la mise à jour du mot de passe.';
        this.loading = false;
      }
    });
  }
}
