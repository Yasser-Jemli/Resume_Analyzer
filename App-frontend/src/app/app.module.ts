import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeadersComponent } from './headers/headers.component';
import { HomeComponent } from './home/home.component';
import { NouveauterComponent } from './nouveauter/nouveauter.component';
import { TestMonCvComponent } from './test-mon-cv/test-mon-cv.component';
import { AboutNousComponent } from './about-nous/about-nous.component';
import { CreationCVComponent } from './creation-cv/creation-cv.component';
import { SafePipe } from './pipes/safe.pipe';
import { NgxExtendedPdfViewerModule } from 'ngx-extended-pdf-viewer';
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
import { ChatAssistantComponent } from './chat-assistant/chat-assistant.component';
import { ConfirmCodeComponent } from './confirm-code/confirm-code.component';
import { UpdatepasswordManagerComponent } from './updatepassword-manager/updatepassword-manager.component';


@NgModule({
  declarations: [
    AppComponent,
    HeadersComponent,
    HomeComponent,
    NouveauterComponent,
    TestMonCvComponent,
    AboutNousComponent,
    CreationCVComponent,
    SafePipe,
    ChatBotComponent,
    LogInComponent,
    SignupComponent,
    ForgotPasswordComponent,
    GestionManagersComponent,
    UserProfileComponent,
    UpdatePasswordComponent,
    ManagerProfileComponent,
    ShowCvuserComponent,
    MypostComponent,
    ChatAssistantComponent,
    ConfirmCodeComponent,
    UpdatepasswordManagerComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxExtendedPdfViewerModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [AuthGuard],
  exports: [SafePipe],
  // Ensure SafePipe is available for use in other components
  bootstrap: [AppComponent,CreationCVComponent]
})
export class AppModule { }