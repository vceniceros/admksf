import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsortiumGridComponent } from './consortium-grid.component';

describe('ConsortiumGridComponent', () => {
  let component: ConsortiumGridComponent;
  let fixture: ComponentFixture<ConsortiumGridComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConsortiumGridComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConsortiumGridComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
