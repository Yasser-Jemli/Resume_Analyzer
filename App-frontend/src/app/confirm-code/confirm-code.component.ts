import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserServiceService } from '../service/user-service.service';

@Component({
  selector: 'app-confirm-code',
  templateUrl: './confirm-code.component.html'
})
export class ConfirmCodeComponent implements OnInit {
  email: string = '';
  code: string = '';
  errorMessage: string | null = null;
  resendSuccessMessage: string | null = null;
  loading: boolean = false;
  sendCodeLoading: boolean = false;
  codeInvalid: boolean = false;
  mode: string = 'signup';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserServiceService
  ) {
    this.route.queryParams.subscribe(params => {
      this.email = params['email'] || '';
      this.mode = params['mode'] || '';

      if (!this.mode) {
        const url = this.router.url;
        if (url.includes('forgot-password')) {
          this.mode = 'forget';
        } else if (url.includes('signup')) {
          this.mode = 'signup';
        } else if (url.includes('login')) {
          this.mode = 'login';
        }
      }

      console.log('Mode actuel dans confirm-code:', this.mode);
    });
  }

  ngOnInit(): void {
    console.log('Email dans confirm-code:', this.email);
    console.log('je suis in int');
    console.log('Mode dans confirm-code:', this.mode);
    if (this.email && this.mode === 'signup') {
      console.log('Envoi du code de confirmation pour le mode login:', this.email);
      this.userService.sendCode(this.email).subscribe({
        next: () => {
          this.sendCodeLoading = false;
          this.resendSuccessMessage = 'Un code de confirmation a été envoyé à votre adresse email.';
        },
        error: () => {
          this.sendCodeLoading = false;
          this.errorMessage = 'Échec de l’envoi du code lors du login.';
        }
      });
    }
  }

  onSubmit(): void {
    this.errorMessage = null;
    this.codeInvalid = false;

    if (!this.code.trim()) {
      this.codeInvalid = true;
      return;
    }

    this.loading = true;

    this.userService.verifyCode({ email: this.email, code: this.code }).subscribe({
      next: () => {
        switch (this.mode) {
          case 'signup':
            const userData = JSON.parse(localStorage.getItem('pendingUser') || '{}');
            if (userData && userData.username && userData.email && userData.password && userData.role) {
              this.userService.createUser(userData).subscribe({
                next: () => {
                  localStorage.removeItem('pendingUser');
                  this.loading = false;
                  this.router.navigate(['/log-in']);
                },
                error: () => {
                  this.loading = false;
                  this.errorMessage = 'Échec de l’inscription. Veuillez réessayer.';
                }
              });
            } else {
              this.loading = false;
              this.router.navigate(['/log-in']);
            }
            break;

          case 'forget':
            const forgetUser = JSON.parse(localStorage.getItem('pendingForgetUser') || '{}');
            this.loading = false;
            if (forgetUser && forgetUser.id) {
              this.router.navigate(['/update-password'], {
                queryParams: { email: this.email, id: forgetUser.id }
              });
            } else {
              console.error('No user ID found in pendingForgetUser:', forgetUser);
              this.errorMessage = 'Impossible de récupérer l\'identifiant utilisateur pour la réinitialisation du mot de passe.';
            }
            break;

          case 'login':
            this.loading = false;
            this.router.navigate(['/dashboard']);
            break;

          default:
            this.loading = false;
            this.errorMessage = 'Mode inconnu. Veuillez réessayer.';
        }
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Code de confirmation invalide. Veuillez réessayer.';
      }
    });
  }

  resendCode(event: Event): void {
    event.preventDefault();
    this.resendSuccessMessage = null;
    this.errorMessage = null;

    this.userService.sendCode(this.email).subscribe({
      next: () => {
        this.resendSuccessMessage = 'Un nouveau code a été envoyé à votre adresse email.';
      },
      error: () => {
        this.errorMessage = 'Erreur lors de l’envoi du code. Veuillez réessayer.';
      }
    });
  }

  updatePassword(user: any, newPassword: string): void {
    this.userService.updateUser(user.id, { password: newPassword }).subscribe({
      next: () => {
        this.router.navigate(['/log-in']);
      },
      error: () => {
        this.errorMessage = 'Erreur lors de la mise à jour du mot de passe. Veuillez réessayer.';
      }
    });
  }
}
