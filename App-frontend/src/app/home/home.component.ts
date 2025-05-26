import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  images = [
    '../../assets/homeimage.png',
    '../../assets/1homeimage.png' // Remplace par le chemin de ta 2ème image
  ];
  currentImage = this.images[0];
  fadeIn = true;

  ngOnInit(): void {
    let index = 0;
    setInterval(() => {
      this.fadeIn = false;
      setTimeout(() => {
        index = (index + 1) % this.images.length;
        this.currentImage = this.images[index];
        this.fadeIn = true;
      }, 500); // fade out duration
    }, 3000); // change image every 3 seconds
  }

}
