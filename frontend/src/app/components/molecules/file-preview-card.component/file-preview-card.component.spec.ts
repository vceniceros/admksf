import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilePreviewCardComponent } from './file-preview-card.component';

describe('FilePreviewCardComponent', () => {
  let component: FilePreviewCardComponent;
  let fixture: ComponentFixture<FilePreviewCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilePreviewCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FilePreviewCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
