import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { UnitsService } from '../../../services/units.service';
import { Unit } from '../../../../models/unit.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { UnitsTableComponent } from '../../molecules/units-table.component/units-table.component';
import { ConsortiumService } from '../../../services/consortium.service';
import { ApiErrorService } from '../../../services/api-error.service';

@Component({
  selector: 'app-units',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LabelComponent,
    IconComponent,
    UnitsTableComponent
  ],
  templateUrl: './units.html',
  styleUrl: './units.css',
  standalone: true
})
export class Units implements OnInit {
  consortiumName: string = '';
  consortiumId: string = '';
  units: Unit[] = [];

  showFormModal = false;
  showDeleteModal = false;
  isEditMode = false;
  selectedUnit: Unit | null = null;
  unitToDelete: Unit | null = null;
  form: FormGroup;
  estados = ['Propietario', 'Inquilino', 'Vacio'];
  tipos = ['Departamento', 'Lote', 'PH'];

  constructor(
    private route: ActivatedRoute,
    private unitsService: UnitsService,
    private consortiumService: ConsortiumService,
    private apiErrorService: ApiErrorService,
    private fb: FormBuilder
  ) {
    this.form = this.fb.group({
      numero_de_unidad_funcional: ['', [Validators.required, Validators.min(1)]],
      consorcio: [{ value: '', disabled: true }, [Validators.required]],
      tipo_de_unidad: ['', Validators.required],
      estado_de_vivienda: ['', Validators.required],
      superficie: ['', [Validators.required, Validators.min(0.01)]],
      propietario: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      this.loadConsortiumData();
    });
  }

  loadConsortiumData() {
    this.consortiumService.getAllConsortiums().subscribe({
      next: (consortia) => {
        const decodedName = decodeURIComponent(this.consortiumName.replace(/-/g, ' '));
        const found = consortia.find(c => c.name.toLowerCase() === decodedName.toLowerCase());
        if (found) {
          this.consortiumId = String(found.id);
          this.form.patchValue({ consorcio: this.consortiumId });
          this.loadUnits();
        }
      },
      error: (error) => {
        console.error('Error loading consortium:', error);
      }
    });
  }

  loadUnits() {
    if (!this.consortiumId) {
      return;
    }
    this.unitsService.getUnitsByConsortium(this.consortiumId).subscribe({
      next: (data) => {
        this.units = data;
      },
      error: (error) => {
        console.error('Error loading units:', error);
      }
    });
  }

  openCreateModal() {
    this.isEditMode = false;
    this.selectedUnit = null;
    this.form.reset({
      numero_de_unidad_funcional: '',
      consorcio: this.consortiumId,
      tipo_de_unidad: '',
      estado_de_vivienda: '',
      superficie: '',
      propietario: ''
    });
    this.showFormModal = true;
  }

  openEditModal(unit: Unit) {
    this.isEditMode = true;
    this.selectedUnit = unit;
    this.showFormModal = true;
    this.form.reset({
      numero_de_unidad_funcional: unit.numero,
      consorcio: unit.consorcio || this.consortiumId,
      tipo_de_unidad: unit.tipo_de_unidad,
      estado_de_vivienda: unit.estado_de_vivienda,
      superficie: unit.superficie,
      propietario: unit.propietario || ''
    });

    this.unitsService.getUnitByNumber(unit.numero).subscribe({
      next: (fullUnit) => {
        if (fullUnit) {
          this.form.patchValue({
            numero_de_unidad_funcional: fullUnit.numero,
            consorcio: fullUnit.consorcio || this.consortiumId,
            tipo_de_unidad: fullUnit.tipo_de_unidad,
            estado_de_vivienda: fullUnit.estado_de_vivienda,
            superficie: fullUnit.superficie,
            propietario: fullUnit.propietario || ''
          });
        }
      },
      error: (error) => {
        console.error('Error loading unit detail:', error);
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
    const payload = {
      consorcio: String(raw.consorcio ?? '').trim(),
      tipo_de_unidad: raw.tipo_de_unidad,
      estado_de_vivienda: raw.estado_de_vivienda,
      superficie: raw.superficie,
      propietario: String(raw.propietario ?? '').trim()
    };

    if (this.isEditMode && this.selectedUnit) {
      this.unitsService.updateUnit(this.selectedUnit.numero, payload).subscribe({
        next: () => {
          this.closeFormModal();
          this.loadUnits();
        },
        error: (error) => {
          const message = this.apiErrorService.extractDetailedMessage(error, 'Error al actualizar unidad funcional.');
          alert(message);
          console.error('Error updating unit:', error);
        }
      });
      return;
    }

    const createPayload = {
      numero_de_unidad_funcional: Number(raw.numero_de_unidad_funcional),
      ...payload
    };

    this.unitsService.createUnit(createPayload).subscribe({
      next: () => {
        this.closeFormModal();
        this.loadUnits();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al crear unidad funcional.');
        alert(message);
        console.error('Error creating unit:', error);
      }
    });
  }

  onDeleteUnit(unit: Unit) {
    this.unitToDelete = unit;
    this.showDeleteModal = true;
  }

  closeDeleteModal() {
    this.showDeleteModal = false;
    this.unitToDelete = null;
  }

  confirmDelete() {
    if (!this.unitToDelete) {
      return;
    }
    this.unitsService.deleteUnit(this.unitToDelete.numero).subscribe({
      next: () => {
        this.closeDeleteModal();
        this.loadUnits();
      },
      error: (error) => {
        const message = this.apiErrorService.extractDetailedMessage(error, 'Error al eliminar unidad funcional.');
        alert(message);
        console.error('Error deleting unit:', error);
      }
    });
  }
}
