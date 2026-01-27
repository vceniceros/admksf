import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatusLabelComponent } from './status-label.component';

describe('StatusLabelComponent', () => {
  let component: StatusLabelComponent;
  let fixture: ComponentFixture<StatusLabelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatusLabelComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StatusLabelComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
