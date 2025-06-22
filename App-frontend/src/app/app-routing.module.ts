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
import { AuthGuard } from './auth.guard';
import { GestionManagersComponent } from './gestion-managers/gestion-managers.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { UpdatePasswordComponent } from './update-password/update-password.component';
import { ManagerProfileComponent } from './manager-profile/manager-profile.component';
import { ShowCvuserComponent } from './show-cvuser/show-cvuser.component';
import { MypostComponent } from './mypost/mypost.component';
import { ConfirmCodeComponent } from './confirm-code/confirm-code.component';
import { UpdatepasswordManagerComponent } from './updatepassword-manager/updatepassword-manager.component';

const routes: Routes = [
  { path: '', redirectTo: '/log-in', pathMatch: 'full' },
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },

  { 
    path: 'nouveauter', 
    component: NouveauterComponent,
     canActivate: [AuthGuard],
    data: { roles: ['CANDIDATE']}

  },

  { 
    path: 'test-mon-cv',
    component: TestMonCvComponent, 
    canActivate: [AuthGuard],
    data: { roles: ['CANDIDATE'] }
  },

  { 
    path: 'creation-cv', 
    component: CreationCVComponent, 
    canActivate: [AuthGuard],
    data: { roles: ['CANDIDATE'] }
  },

  { 
    path: 'about-nous', 
    component: AboutNousComponent, 
    canActivate: [AuthGuard] ,
    data: { roles: ['CANDIDATE'] }
  },

  { 
    path: 'chat-bot', 
    component: ChatBotComponent, 
    canActivate: [AuthGuard],
    data: { roles: ['CANDIDATE'] }
   },

  { 
    path: 'gestion-managers', 
    component: GestionManagersComponent, 
    canActivate: [AuthGuard], 
    data: { roles: ['SYSADMIN'] } 
  },
  
  { path: 'log-in', 
    component: LogInComponent 
  },

  { path: 'signup', 
    component: SignupComponent 
  },

  { path: 'forgot-password', 
    component: ForgotPasswordComponent 
  },
  
  { 
    path: 'update-password', 
    component: UpdatePasswordComponent},
  { 
    path : 'confirm-code', 
    component: ConfirmCodeComponent
  }, 
  { path: 'not-found', component: NotFoundComponent },
  { 
    path: 'profile/:id', 
    component: UserProfileComponent, 
    canActivate: [AuthGuard],
    data: { roles: ['CANDIDATE'] }
  },
  { 
    path: 'manager-profile/:id',
    component: ManagerProfileComponent, 
    canActivate: [AuthGuard], 
    data: { roles: ['MANAGER'] } 
  },
  { 
    path: 'showCVuser', 
    component: ShowCvuserComponent, 
    canActivate: [AuthGuard], 
    data: { roles: ['MANAGER'] } 
  },
  { 
    path: 'Mypost', 
    canActivate: [AuthGuard],
    component: MypostComponent , 
    data: { roles: ['MANAGER']}
  },
  { 
    path : 'update-password-manager',
    component: UpdatepasswordManagerComponent, 
    canActivate: [AuthGuard] ,
    data: { roles: ['MANAGER'] }
  },
  { path: '**', redirectTo: '/not-found' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
