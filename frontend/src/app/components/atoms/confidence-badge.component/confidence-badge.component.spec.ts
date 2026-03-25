import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfidenceBadgeComponent } from './confidence-badge.component';

describe('ConfidenceBadgeComponent', () => {
  let component: ConfidenceBadgeComponent;
  let fixture: ComponentFixture<ConfidenceBadgeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConfidenceBadgeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConfidenceBadgeComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
