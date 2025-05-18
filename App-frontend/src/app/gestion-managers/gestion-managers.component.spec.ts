import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionManagersComponent } from './gestion-managers.component';

describe('GestionManagersComponent', () => {
  let component: GestionManagersComponent;
  let fixture: ComponentFixture<GestionManagersComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GestionManagersComponent]
    });
    fixture = TestBed.createComponent(GestionManagersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
