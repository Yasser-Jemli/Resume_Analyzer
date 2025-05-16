import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreationCVComponent } from './creation-cv.component';

describe('CreationCVComponent', () => {
  let component: CreationCVComponent;
  let fixture: ComponentFixture<CreationCVComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CreationCVComponent]
    });
    fixture = TestBed.createComponent(CreationCVComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
