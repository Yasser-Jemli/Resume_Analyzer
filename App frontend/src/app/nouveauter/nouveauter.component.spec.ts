import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NouveauterComponent } from './nouveauter.component';

describe('NouveauterComponent', () => {
  let component: NouveauterComponent;
  let fixture: ComponentFixture<NouveauterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NouveauterComponent]
    });
    fixture = TestBed.createComponent(NouveauterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
