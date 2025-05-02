import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

@Component({
  selector: 'app-creation-cv',
  templateUrl: './creation-cv.component.html',
  styleUrls: ['./creation-cv.component.css']
})
export class CreationCVComponent {
  @ViewChild('cvContent') cvContent!: ElementRef;
  cvForm: FormGroup;
  submitted = false;
  pdfSrc: string = '';

  constructor(private fb: FormBuilder) {
    this.cvForm = this.fb.group({
      personalInfo: this.fb.group({
        nom: ['', Validators.required],
        prenom: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        telephone: ['', Validators.required],
        adresse: ['', Validators.required],
        dateNaissance: ['', Validators.required]
      }),
      formation: this.fb.array([
        this.fb.group({
          diplome: ['', Validators.required],
          etablissement: ['', Validators.required],
          dateDebut: ['', Validators.required],
          dateFin: ['', Validators.required],
          description: ['']
        })
      ]),
      experience: this.fb.array([
        this.fb.group({
          poste: ['', Validators.required],
          entreprise: ['', Validators.required],
          dateDebut: ['', Validators.required],
          dateFin: ['', Validators.required],
          description: ['']
        })
      ]),
      competences: this.fb.array([
        this.fb.group({
          nom: ['', Validators.required],
          niveau: ['', Validators.required]
        })
      ]),
      langues: this.fb.array([
        this.fb.group({
          langue: ['', Validators.required],
          niveau: ['', Validators.required]
        })
      ])
    });
  }

  get personalInfo() {
    return this.cvForm.get('personalInfo') as FormGroup;
  }

  get formation() {
    return this.cvForm.get('formation') as any;
  }

  get experience() {
    return this.cvForm.get('experience') as any;
  }

  get competences() {
    return this.cvForm.get('competences') as any;
  }

  get langues() {
    return this.cvForm.get('langues') as any;
  }

  addFormation() {
    this.formation.push(this.fb.group({
      diplome: ['', Validators.required],
      etablissement: ['', Validators.required],
      dateDebut: ['', Validators.required],
      dateFin: ['', Validators.required],
      description: ['']
    }));
  }

  addExperience() {
    this.experience.push(this.fb.group({
      poste: ['', Validators.required],
      entreprise: ['', Validators.required],
      dateDebut: ['', Validators.required],
      dateFin: ['', Validators.required],
      description: ['']
    }));
  }

  addCompetence() {
    this.competences.push(this.fb.group({
      nom: ['', Validators.required],
      niveau: ['', Validators.required]
    }));
  }

  addLangue() {
    this.langues.push(this.fb.group({
      langue: ['', Validators.required],
      niveau: ['', Validators.required]
    }));
  }

  removeFormation(index: number) {
    this.formation.removeAt(index);
  }

  removeExperience(index: number) {
    this.experience.removeAt(index);
  }

  removeCompetence(index: number) {
    this.competences.removeAt(index);
  }

  removeLangue(index: number) {
    this.langues.removeAt(index);
  }

  async onSubmit() {
    this.submitted = true;
    if (this.cvForm.valid) {
      const content = this.cvContent.nativeElement;
      const canvas = await html2canvas(content);
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgWidth = 210;
      const imgHeight = canvas.height * imgWidth / canvas.width;

      pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
      pdf.save('mon-cv.pdf');
    }
  }

  exportToJson() {
    if (this.cvForm.valid) {
      const cvData = this.cvForm.value;
      const jsonString = JSON.stringify(cvData, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'mon-cv.json';
      link.click();
      window.URL.revokeObjectURL(url);
    } else {
      this.submitted = true;
    }
  }
}
