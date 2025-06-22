// src/app/auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role') || '';
    const allowedRoles = route.data['roles'] as string[];
    console.log('token:', token);
    console.log('User Role:', role);
    console.log('Allowed Roles:', allowedRoles);
    if (allowedRoles && !allowedRoles.includes(role)) {
      this.router.navigate(['/not-found']);
      return false;
    }

    if (token) {
      return true;
    } else {
      this.router.navigate(['/log-in']);
      return false;
    }
  }
}
