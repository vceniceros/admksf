import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GenericButtonComponent } from './generic-button.component';

describe('GenericButtonComponent', () => {
  let component: GenericButtonComponent;
  let fixture: ComponentFixture<GenericButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GenericButtonComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GenericButtonComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
