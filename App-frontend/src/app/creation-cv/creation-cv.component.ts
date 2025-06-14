import { Component, ElementRef, ViewChild, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray } from '@angular/forms';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
// 👉 Importe ici ton service utilisateur si tu veux sauvegarder le CV côté backend
import { UserServiceService } from '../service/user-service.service';

@Component({
  selector: 'app-creation-cv',
  templateUrl: './creation-cv.component.html',
  styleUrls: ['./creation-cv.component.css']
})
export class CreationCVComponent implements OnInit {
  @ViewChild('cvContent') cvContent!: ElementRef;
  cvForm: FormGroup;
  submitted = false;
  lastGeneratedCV: any;

  constructor(
    private fb: FormBuilder,
    private userService: UserServiceService // <-- Injection du service utilisateur
  ) {
    this.cvForm = this.fb.group({
      personalInfo: this.fb.group({
        nom: [''],
        prenom: [''],
        email: [''],
        telephone: [''],
        adresse: [''],
        dateNaissance: ['']
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

  // Getters
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

  // Controls access
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

  // Add items
  addFormation() {
    this.formation.push(this.fb.group({
      diplome: [''],
      etablissement: [''],
      dateDebut: [''],
      dateFin: [''],
      description: ['']
    }));
  }
  addExperience() {
    this.experience.push(this.fb.group({
      poste: [''],
      entreprise: [''],
      dateDebut: [''],
      dateFin: [''],
      description: ['']
    }));
  }
  addCompetence() {
    this.competences.push(this.fb.group({
      nom: [''],
      niveau: ['']
    }));
  }
  addLangue() {
    this.langues.push(this.fb.group({
      langue: [''],
      niveau: ['']
    }));
  }

  // Remove items
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

  // Generate CV
  async generateCV() {
    try {
      this.submitted = true;

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

      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save('mon-cv.pdf');

      const cvData = this.cvForm.value;
      const jsonBlob = new Blob([JSON.stringify(cvData, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(jsonBlob);
      const link = document.createElement('a');
      link.href = url;
      //link.download = 'mon-cv.json';
      //link.click();
      window.URL.revokeObjectURL(url);

      console.log('CV généré :', cvData);
      this.lastGeneratedCV = this.cvForm.value;

      // 👉 Exemple d'utilisation du service pour sauvegarder le CV côté backend (optionnel)
      // this.userService.updateUser(userId, { cvData }).subscribe({
      //   next: (res) => console.log('CV sauvegardé côté backend', res),
      //   error: (err) => console.error('Erreur sauvegarde backend', err)
      // });

    } catch (error) {
      console.error('Erreur lors de la génération du CV :', error);
      alert('Une erreur est survenue lors de la génération du CV.');
    }
  }

  // Accès dynamique pour affichage (on ne peut pas utiliser this dans l’objet)
  get sections() {
    return [
      {
        label: 'Formations',
        fields: [
          { name: 'diplome', type: 'text', label: 'Diplôme' },
          { name: 'etablissement', type: 'text', label: 'Établissement' },
          { name: 'dateDebut', type: 'date', label: 'Date début' },
          { name: 'dateFin', type: 'date', label: 'Date fin' },
          { name: 'description', type: 'textarea', label: 'Description' }
        ],
        getControls: () => this.getFormationControls(),
        add: () => this.addFormation(),
        remove: (i: number) => this.removeFormation(i)
      },
      {
        label: 'Expériences',
        fields: [
          { name: 'poste', type: 'text', label: 'Poste' },
          { name: 'entreprise', type: 'text', label: 'Entreprise' },
          { name: 'dateDebut', type: 'date', label: 'Date début' },
          { name: 'dateFin', type: 'date', label: 'Date fin' },
          { name: 'description', type: 'textarea', label: 'Description' }
        ],
        getControls: () => this.getExperienceControls(),
        add: () => this.addExperience(),
        remove: (i: number) => this.removeExperience(i)
      },
      {
        label: 'Compétences',
        fields: [
          { name: 'nom', type: 'text', label: 'Nom' },
          { name: 'niveau', type: 'text', label: 'Niveau' }
        ],
        getControls: () => this.getCompetencesControls(),
        add: () => this.addCompetence(),
        remove: (i: number) => this.removeCompetence(i)
      },
      {
        label: 'Langues',
        fields: [
          { name: 'langue', type: 'text', label: 'Langue' },
          { name: 'niveau', type: 'text', label: 'Niveau' }
        ],
        getControls: () => this.getLanguesControls(),
        add: () => this.addLangue(),
        remove: (i: number) => this.removeLangue(i)
      }
    ];
  }
}
