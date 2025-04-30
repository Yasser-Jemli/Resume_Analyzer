import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeadrsComponent } from './headrs/headrs.component';
import { HomeComponent } from './home/home.component';
import { NouveauterComponent } from './nouveauter/nouveauter.component';
import { TestMonCvComponent } from './test-mon-cv/test-mon-cv.component';
import { AboutNousComponent } from './about-nous/about-nous.component';
import { CreationCVComponent } from './creation-cv/creation-cv.component';
import { SafePipe } from './pipes/safe.pipe';
import { NgxExtendedPdfViewerModule } from 'ngx-extended-pdf-viewer';

@NgModule({
  declarations: [
    AppComponent,
    HeadrsComponent,
    HomeComponent,
    NouveauterComponent,
    TestMonCvComponent,
    AboutNousComponent,
    CreationCVComponent,
    SafePipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxExtendedPdfViewerModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }