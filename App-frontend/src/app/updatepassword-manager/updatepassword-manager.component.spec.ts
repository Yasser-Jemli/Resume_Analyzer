import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdatepasswordManagerComponent } from './updatepassword-manager.component';

describe('UpdatepasswordManagerComponent', () => {
  let component: UpdatepasswordManagerComponent;
  let fixture: ComponentFixture<UpdatepasswordManagerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UpdatepasswordManagerComponent]
    });
    fixture = TestBed.createComponent(UpdatepasswordManagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
