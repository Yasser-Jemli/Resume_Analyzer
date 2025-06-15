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
    this.userService.getUserByUsername(this.username).subscribe(users => {
      if (users.length > 0) {
        const user = users[0];
        // Met à jour le mot de passe
        this.userService.updateUser(user.id, {
          password: this.newPassword?.value
        }).subscribe({
          next: () => {
            // Met à jour le flag ChangePassword à true (ou passwordChanged à true)
            this.userService.changePasswordFlag(user.id, false).subscribe({
              next: () => {
                this.successMessage = 'Mot de passe mis à jour avec succès !';
                this.loading = false;
                setTimeout(() => this.router.navigate(['/manager-profile']), 1500);
              },
              error: () => {
                this.errorMessage = 'Erreur lors de la mise à jour du statut du mot de passe.';
                this.loading = false;
              }
            });
          },
          error: () => {
            this.errorMessage = 'Erreur lors de la mise à jour du mot de passe.';
            this.loading = false;
          }
        });
      } else {
        this.errorMessage = 'Utilisateur introuvable.';
        this.loading = false;
      }
    }, () => {
      this.errorMessage = 'Erreur lors de la recherche de l\'utilisateur.';
      this.loading = false;
    });
  }
}
