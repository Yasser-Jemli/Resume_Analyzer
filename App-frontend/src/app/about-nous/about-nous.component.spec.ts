import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AboutNousComponent } from './about-nous.component';

describe('AboutNousComponent', () => {
  let component: AboutNousComponent;
  let fixture: ComponentFixture<AboutNousComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AboutNousComponent]
    });
    fixture = TestBed.createComponent(AboutNousComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
