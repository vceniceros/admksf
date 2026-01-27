import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileStoreInputComponent } from './file-store-input.component';

describe('FileStoreInputComponent', () => {
  let component: FileStoreInputComponent;
  let fixture: ComponentFixture<FileStoreInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FileStoreInputComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FileStoreInputComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
