// src/app/app-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { NouveauterComponent } from './nouveauter/nouveauter.component';
import { TestMonCvComponent } from './test-mon-cv/test-mon-cv.component';
import { AboutNousComponent } from './about-nous/about-nous.component';
import { CreationCVComponent } from './creation-cv/creation-cv.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ChatBotComponent } from './chat-bot/chat-bot.component';
import { LogInComponent } from './log-in/log-in.component';
import { SignupComponent } from './signup/signup.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { AuthGuard } from './auth.guard'; // 👈 Ajout ici

const routes: Routes = [
  { path: '', redirectTo: '/log-in', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'nouveauter', component: NouveauterComponent, canActivate: [AuthGuard] },
  { path: 'test-mon-cv', component: TestMonCvComponent, canActivate: [AuthGuard] },
  { path: 'creation-cv', component: CreationCVComponent, canActivate: [AuthGuard] },
  { path: 'about-nous', component: AboutNousComponent, canActivate: [AuthGuard] },
  { path: 'chat-bot', component: ChatBotComponent, canActivate: [AuthGuard] },
  { path: 'log-in', component: LogInComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'not-found', component: NotFoundComponent },
  { path: '**', redirectTo: '/not-found' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
