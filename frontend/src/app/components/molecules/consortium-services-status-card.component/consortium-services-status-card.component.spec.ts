import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumServicesStatusCardComponent } from './consortium-services-status-card.component';

describe('ConsortiumServicesStatusCardComponent', () => {
  let component: ConsortiumServicesStatusCardComponent;
  let fixture: ComponentFixture<ConsortiumServicesStatusCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumServicesStatusCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumServicesStatusCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
