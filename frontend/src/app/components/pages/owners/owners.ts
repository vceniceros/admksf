import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { OwnersService } from '../../../services/owners.service';
import { ApiErrorService } from '../../../services/api-error.service';
import { Owner } from '../../../../models/owner.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { OwnersTableComponent } from '../../molecules/owners-table.component/owners-table.component';

@Component({
  selector: 'app-owners',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LabelComponent,
    IconComponent,
    OwnersTableComponent
  ],
  templateUrl: './owners.html',
  styleUrl: './owners.css',
  standalone: true
})
export class Owners implements OnInit {
  consortiumName: string = '';
  owners: Owner[] = [];

  showFormModal = false;
  showDeleteModal = false;
  isEditMode = false;
  selectedOwner: Owner | null = null;
  ownerToDelete: Owner | null = null;
  form: FormGroup;

  constructor(
    private route: ActivatedRoute,
    private ownersService: OwnersService,
    private apiErrorService: ApiErrorService,
    private fb: FormBuilder
  ) {
    this.form = this.fb.group({
      dni: ['', [Validators.required, Validators.pattern(/^\d+$/)]],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      telefono: [''],
      email: ['', Validators.email]
    });
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      this.loadOwners();
    });
  }

  loadOwners() {
    this.ownersService.getAllOwners().subscribe({
      next: (data) => {
        this.owners = data;
      },
      error: (error) => {
        console.error('Error loading owners:', error);
      }
    });
  }

  openCreateModal() {
    this.isEditMode = false;
    this.selectedOwner = null;
    this.form.reset({
      dni: '',
      nombre: '',
      apellido: '',
      telefono: '',
      email: ''
    });
    this.showFormModal = true;
  }

  openEditModal(owner: Owner) {
    this.isEditMode = true;
    this.selectedOwner = owner;
    this.showFormModal = true;
    this.form.reset({
      dni: owner.dni,
      nombre: owner.nombre,
      apellido: owner.apellido,
      telefono: owner.telefono ?? '',
      email: owner.email ?? ''
    });

    this.ownersService.getOwnerByDni(owner.dni).subscribe({
      next: (fullOwner) => {
        if (fullOwner) {
          this.form.patchValue({
            dni: fullOwner.dni,
            nombre: fullOwner.nombre,
            apellido: fullOwner.apellido,
            telefono: fullOwner.telefono ?? '',
            email: fullOwner.email ?? ''
          });
        }
      },
      error: (error) => {
        console.error('Error loading owner detail:', error);
      }
    });
  }

  closeFormModal() {
    this.showFormModal = false;
  }

  submitForm() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const raw = this.form.getRawValue();
    const dni = String(raw.dni ?? '').trim();
    const normalizedDni = dni.replace(/\D/g, '');
    const payload = {
      nombre: raw.nombre,
      apellido: raw.apellido,
      telefono: raw.telefono || null,
      email: raw.email || null
    };

    if (this.isEditMode && this.selectedOwner) {
      this.ownersService.updateOwner(this.selectedOwner.dni, payload).subscribe({
        next: () => {
          this.closeFormModal();
          this.loadOwners();
        },
        error: (error) => {
          const message = this.apiErrorService.extractDetailedMessage(error, 'Error al actualizar propietario.');
          alert(message);
          console.error('Error updating owner:', error);
        }
      });
      return;
    }

    const createPayload = {
      dni: normalizedDni,
      ...payload
    };

    this.ownersService.createOwner(createPayload).subscribe({
      next: () => {
        this.closeFormModal();
        this.loadOwners();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al crear propietario.');
        alert(message);
        console.error('Error creating owner:', error);
      }
    });
  }

  onDeleteOwner(owner: Owner) {
    this.ownerToDelete = owner;
    this.showDeleteModal = true;
  }

  closeDeleteModal() {
    this.showDeleteModal = false;
    this.ownerToDelete = null;
  }

  confirmDelete() {
    if (!this.ownerToDelete) {
      return;
    }
    this.ownersService.deleteOwner(this.ownerToDelete.dni).subscribe({
      next: () => {
        this.closeDeleteModal();
        this.loadOwners();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al eliminar propietario.');
        alert(message);
        console.error('Error deleting owner:', error);
      }
    });
  }
}
