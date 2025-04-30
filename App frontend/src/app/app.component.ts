import { Component } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NotFoundComponent } from './not-found/not-found.component';
import { HomeComponent } from './home/home.component';
//import { NouveauterComponent } from './nouveauter/nouveauter.component'; // Import NouveauterComponent

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Redirect default path to /home
  { path: 'home', component: HomeComponent } ,// Home route
  //{patheauté", component: NouveauterComponent}, : "/nouv
];

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Mission_Entreprise_Angular';
}
