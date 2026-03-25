import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DropZoneComponent } from './drop-zone.component';

describe('DropZoneComponent', () => {
  let component: DropZoneComponent;
  let fixture: ComponentFixture<DropZoneComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DropZoneComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DropZoneComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
