import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface PersonalInfo {
  nom: string;
  prenom: string;
  email: string;
  telephone: string;
  adresse: string;
  dateNaissance: string;
}

interface Formation {
  diplome: string;
  etablissement: string;
  dateDebut: string;
  dateFin: string;
  description: string;
}

interface Experience {
  poste: string;
  entreprise: string;
  dateDebut: string;
  dateFin: string;
  description: string;
}

interface Competence {
  nom: string;
  niveau: string;
}

interface Langue {
  langue: string;
  niveau: string;
}

@Component({
  selector: 'app-creation-cv',
  templateUrl: './creation-cv.component.html',
  styleUrls: ['./creation-cv.component.css']
})
export class CreationCVComponent {
  @ViewChild('cvContent') cvContent!: ElementRef;
  cvForm: FormGroup;
  submitted = false;

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
      formation: this.fb.array([]),
      experience: this.fb.array([]),
      competences: this.fb.array([]),
      langues: this.fb.array([])
    });
  }

  ngOnInit() {
    this.addFormation();
    this.addExperience();
    this.addCompetence();
    this.addLangue();
  }

  get personalInfo(): FormGroup {
    return this.cvForm.get('personalInfo') as FormGroup;
  }

  get formation(): FormArray {
    return this.cvForm.get('formation') as FormArray;
  }

  get experience(): FormArray {
    return this.cvForm.get('experience') as FormArray;
  }

  get competences(): FormArray {
    return this.cvForm.get('competences') as FormArray;
  }

  get langues(): FormArray {
    return this.cvForm.get('langues') as FormArray;
  }

  // Helper to cast FormArray controls to FormGroup
  getFormationControls(): FormGroup[] {
    return this.formation.controls as FormGroup[];
  }

  getExperienceControls(): FormGroup[] {
    return this.experience.controls as FormGroup[];
  }

  getCompetencesControls(): FormGroup[] {
    return this.competences.controls as FormGroup[];
  }

  getLanguesControls(): FormGroup[] {
    return this.langues.controls as FormGroup[];
  }

  // Custom validator for date ranges
  dateRangeValidator(group: FormGroup) {
    const dateDebut = group.get('dateDebut')?.value;
    const dateFin = group.get('dateFin')?.value;
    return dateDebut && dateFin && dateDebut > dateFin
      ? { invalidDateRange: true }
      : null;
  }

  addFormation() {
    this.formation.push(this.fb.group({
      diplome: ['', Validators.required],
      etablissement: ['', Validators.required],
      dateDebut: ['', Validators.required],
      dateFin: ['', Validators.required],
      description: ['']
    }, { validators: this.dateRangeValidator }));
  }

  addExperience() {
    this.experience.push(this.fb.group({
      poste: ['', Validators.required],
      entreprise: ['', Validators.required],
      dateDebut: ['', Validators.required],
      dateFin: ['', Validators.required],
      description: ['']
    }, { validators: this.dateRangeValidator }));
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

  async generateCV() {
    try {
      this.submitted = true;
      if (this.cvForm.valid) {
        // Generate PDF with multi-page support
        const content = this.cvContent.nativeElement;
        const canvas = await html2canvas(content, { scale: 2 });
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const imgWidth = 210;
        const pageHeight = 297;
        const imgHeight = canvas.height * imgWidth / canvas.width;
        let heightLeft = imgHeight;
        let position = 0;

        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        while (heightLeft >= 0) {
          position = heightLeft - imgHeight;
          pdf.addPage();
          pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
          heightLeft -= pageHeight;
        }

        pdf.save('mon-cv.pdf');

        // Download JSON
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
        console.log('Form is invalid');
      }
    } catch (error) {
      console.error('Error generating CV:', error);
      alert('Une erreur est survenue lors de la génération du CV.');
    }
  }
}