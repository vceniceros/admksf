import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumDashboardComponent } from './consortium-dashboard.component';

describe('ConsortiumDashboardComponent', () => {
  let component: ConsortiumDashboardComponent;
  let fixture: ComponentFixture<ConsortiumDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumDashboardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
