import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SmartFieldComponent } from './smart-field.component';

describe('SmartFieldComponent', () => {
  let component: SmartFieldComponent;
  let fixture: ComponentFixture<SmartFieldComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SmartFieldComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SmartFieldComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
