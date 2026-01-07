import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumCardComponent } from './consortium-card.component';

describe('ConsortiumCardComponent', () => {
  let component: ConsortiumCardComponent;
  let fixture: ComponentFixture<ConsortiumCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
