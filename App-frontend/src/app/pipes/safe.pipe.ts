import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeResourceUrl, SafeHtml, SafeStyle, SafeScript } from '@angular/platform-browser';

@Pipe({
  name: 'safe'
})
export class SafePipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  /**
   * Transforme et assainit la valeur selon le type donné.
   * @param value - la chaîne à assainir (ex: URL)
   * @param type - type d'assainissement : 'url'|'html'|'style'|'script', default 'url'
   * @returns valeur assainie
   */
  transform(value: string | null | undefined, type: 'url' | 'html' | 'style' | 'script' = 'url'): SafeResourceUrl | SafeHtml | SafeStyle | SafeScript | null {
    if (!value) {
      return null;
    }

    switch (type) {
      case 'html':
        return this.sanitizer.bypassSecurityTrustHtml(value);
      case 'style':
        return this.sanitizer.bypassSecurityTrustStyle(value);
      case 'script':
        return this.sanitizer.bypassSecurityTrustScript(value);
      case 'url':
      default:
        return this.sanitizer.bypassSecurityTrustResourceUrl(value);
    }
  }
} 