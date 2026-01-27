import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpensesEntryTemplateComponent } from './expenses-entry-template.component';

describe('ExpensesEntryTemplateComponent', () => {
  let component: ExpensesEntryTemplateComponent;
  let fixture: ComponentFixture<ExpensesEntryTemplateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExpensesEntryTemplateComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExpensesEntryTemplateComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
