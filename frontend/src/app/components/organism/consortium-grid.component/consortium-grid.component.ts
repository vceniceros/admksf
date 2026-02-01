import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Consortium } from '../../../../models/consortium.model';
import { ConsortiumCardComponent } from '../../molecules/consortium-card.component/consortium-card.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { ConsortiumStatus } from '../../../../models/consortium.model';
import { ConsortiumService } from '../../../services/consortium.service';
import { DropZone } from '../../molecules/drop-zone/drop-zone';
import { FilePreview } from '../../molecules/file-preview/file-preview';

@Component({
  selector: 'app-consortium-grid',
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    ConsortiumCardComponent,
    IconComponent,
    LabelComponent,
    DropZone,
    FilePreview
  ],
  templateUrl: './consortium-grid.component.html',
  styleUrl: './consortium-grid.component.css',
  standalone: true
})
export class ConsortiumGridComponent {
  @Input() consortia!: Consortium[];
  @Output() consortiumCreated = new EventEmitter<void>();
  @Output() consortiumDeleted = new EventEmitter<void>();
  showCreateModal = false;
  showDeleteModal = false;
  consortiumToDelete?: Consortium;
  selectedFile: File | null = null;
  fileName = '';
  form: FormGroup;
  statusOptions = Object.values(ConsortiumStatus);

  constructor(
    private fb: FormBuilder,
    private consortiumService: ConsortiumService
  ) {
    this.form = this.fb.group({
      cuit: ['', [Validators.required, Validators.pattern(/^\d+$/)]],
      razon_social: ['', Validators.required],
      calle: ['', Validators.required],
      numero: [0, [Validators.required, Validators.min(1)]],
      codigo_postal: ['', Validators.required],
      ciudad: ['', Validators.required],
      interes_por_mora: [0, [Validators.required, Validators.min(0)]],
      redondeo_aumento: [0, [Validators.required, Validators.min(0)]]
    });
  }

  onAddConsortium() {
    this.showCreateModal = true;
  }

  closeModal() {
    this.showCreateModal = false;
    this.selectedFile = null;
    this.fileName = '';
    this.form.reset({
      cuit: '',
      razon_social: '',
      calle: '',
      numero: 0,
      codigo_postal: '',
      ciudad: '',
      interes_por_mora: 0,
      redondeo_aumento: 0
    });
  }

  submitCreate() {
    if (this.form.invalid) {
      Object.keys(this.form.controls).forEach(key => this.form.get(key)?.markAsTouched());
      return;
    }
    const payload = this.form.value;
    this.consortiumService.createConsortium(payload).subscribe({
      next: () => {
        if (this.selectedFile) {
          this.consortiumService.uploadConsortiumImage(payload.cuit, this.selectedFile).subscribe({
            next: () => {
              this.closeModal();
              this.consortiumCreated.emit();
            },
            error: (error: any) => {
              alert('Error al subir la imagen.');
              console.error('Error al subir la imagen:', error);
            }
          });
          return;
        }
        this.closeModal();
        this.consortiumCreated.emit();
      },
      error: (error: any) => {
        alert('Error al crear consorcio.');
        console.error('Error al crear consorcio:', error);
      }
    });
  }

  onFileDropped(file: File) {
    if (!file.type.startsWith('image/')) {
      alert('Solo se permiten imágenes.');
      return;
    }
    this.selectedFile = file;
    this.fileName = file.name;
  }

  onFileRemove() {
    this.selectedFile = null;
    this.fileName = '';
  }

  onDeleteConsortium(consortium: Consortium) {
    this.consortiumToDelete = consortium;
    this.showDeleteModal = true;
  }

  closeDeleteModal() {
    this.showDeleteModal = false;
    this.consortiumToDelete = undefined;
  }

  confirmDelete() {
    if (!this.consortiumToDelete) {
      return;
    }
    this.consortiumService.deleteConsortium(this.consortiumToDelete.id).subscribe({
      next: () => {
        this.closeDeleteModal();
        this.consortiumDeleted.emit();
      },
      error: (error: any) => {
        alert('Error al eliminar consorcio.');
        console.error('Error al eliminar consorcio:', error);
      }
    });
  }
}
