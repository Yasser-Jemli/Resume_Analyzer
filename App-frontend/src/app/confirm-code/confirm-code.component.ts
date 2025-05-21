import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-confirm-code',
  templateUrl: './confirm-code.component.html'
})
export class ConfirmCodeComponent {
  email: string = '';
  code: string = '';
  errorMessage: string | null = null;
  resendSuccessMessage: string | null = null;
  loading: boolean = false;
  codeInvalid: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService
  ) {
    this.route.queryParams.subscribe(params => {
      this.email = params['email'] || '';
    });
  }

  onSubmit() {
    this.errorMessage = null;
    this.codeInvalid = false;

    if (!this.code.trim()) {
      this.codeInvalid = true;
      return;
    }

    // Simulated code for testing
    if (this.code === '123456') {
      this.router.navigate(['/log-in']);
      return;
    }

    this.loading = true;

    this.userService.verifyCode({ email: this.email, code: this.code }).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/log-in']);
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Code de confirmation invalide. Veuillez réessayer.';
      }
    });
  }

  resendCode(event: Event) {
    event.preventDefault(); // Prevent navigation
    this.resendSuccessMessage = null;
    this.errorMessage = null;

    this.userService.resendConfirmationCode(this.email).subscribe({
      next: () => {
        this.resendSuccessMessage = 'Un nouveau code a été envoyé à votre adresse email.';
      },
      error: () => {
        this.errorMessage = 'Erreur lors de l’envoi du code. Veuillez réessayer.';
      }
    });
  }
}
