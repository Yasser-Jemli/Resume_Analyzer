import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { JiraServiceService } from '../service/jira-service.service';
import { ChatInterviewServiceService } from '../service/chat-interview-service.service'; // <-- Import du service

interface JiraIssue {
  key: string;
  fields: {
    summary: string;
    description: string;
    customfield_10056?: string; // responsibilities
    customfield_10057?: string; // skills
    customfield_10055?: string; // description
  };
}

@Component({
  selector: 'app-nouveauter',
  templateUrl: './nouveauter.component.html',
  styleUrls: ['./nouveauter.component.css']
})
export class NouveauterComponent implements OnInit {
  issues: JiraIssue[] = [];
  skillsList: string[] = [];
  canIncrementCV: Boolean = false;

  constructor(
    private jiraService: JiraServiceService,
    private chatInterviewService: ChatInterviewServiceService, // <-- Ajouté ici
    private router: Router
  ) {}

  ngOnInit() {
    this.jiraService.getIssues().subscribe(
      data => {
        this.issues = data;
        console.log('Issues:', this.issues);
      },
      error => {
        console.error('Error fetching issues from jira server:', error);
      }
    );
  }

  goToTestMonCV(selectedIssue: JiraIssue) {
    // Afficher toutes les informations du post sélectionné dans la console
    console.log('Informations du post sélectionné :', selectedIssue);

    // Récupérer et stocker les skills dans le localStorage
    const skills = selectedIssue.fields.customfield_10057
      ? selectedIssue.fields.customfield_10057.split(',').map((s: string) => s.trim())
      : [];
    localStorage.setItem('postSkills', JSON.stringify(skills));

    // Stocker le nom du post (summary) dans le localStorage
    localStorage.setItem('postName', selectedIssue.fields.summary);

    // Envoyer les skills au chat bot via le service (mémoire + backend)
    this.chatInterviewService.setSkills(skills);

    // Vérifier la mise à jour côté backend (optionnel)
    // this.chatInterviewService.fetchSkillsFromBackend().subscribe(response => {
    //   console.log('Skills récupérés depuis le backend:', response.skills);
    // });

    console.log('Skills envoyés au chat bot et enregistrés dans le localStorage:', skills);

    this.router.navigate(['/test-mon-cv']);
  }

  onSubmit() {
    // envoie les données de poste choisi au serveur
    
    // Optionnel : activer le flag canIncrementCV
    localStorage.setItem('canIncrementCV', 'true');
  }
}







