import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { SpendsService } from '../../../services/spends.services';
import { EstadoPago } from '../../../../models/spends.model';
import { DropZone } from '../../molecules/drop-zone/drop-zone';
import { FilePreview } from '../../molecules/file-preview/file-preview';
import { ExpenseForm } from '../../organism/expense-form/expense-form';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { ConsortiumService } from '../../../services/consortium.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-expense-upload',
  imports: [
    CommonModule, 
    ReactiveFormsModule, 
    DropZone, 
    FilePreview, 
    ExpenseForm, 
    LabelComponent
  ],
  templateUrl: './expense-upload.html',
  styleUrl: './expense-upload.css',
  standalone: true
})
export class ExpenseUpload implements OnInit {
  selectedFile: File | null = null;
  fileName: string = '';
  expenseForm!: FormGroup;
  consortiumName: string = '';
  consortiumId: string = '';
  isEditMode = false;
  expenseId: number | null = null;
  isExtracting = false;

  constructor(
    private fb: FormBuilder,
    private spendsService: SpendsService,
    private router: Router,
    private route: ActivatedRoute,
    private consortiumService: ConsortiumService
  ) {
    this.expenseForm = this.fb.group({
      cuitConsorcio: ['', Validators.required],
      cuitProveedor: ['', Validators.required],
      periodo: ['', Validators.required],
      tipoGasto: ['', Validators.required],
      descripcion: ['', Validators.required],
      monto: [0, [Validators.required, Validators.min(0.01)]],
      estadoPago: [EstadoPago.PENDIENTE, Validators.required]
    });
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.consortiumName = params['consortiumName'];
      const idParam = params['idGasto'];
      this.expenseId = idParam ? Number(idParam) : null;
      this.isEditMode = !!this.expenseId;
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
          this.expenseForm.patchValue({ cuitConsorcio: this.consortiumId });
          if (this.isEditMode && this.expenseId) {
            this.loadExpense();
          }
        }
      },
      error: (error) => {
        console.error('Error loading consortium:', error);
      }
    });
  }

  loadExpense() {
    if (!this.expenseId) {
      return;
    }
    this.spendsService.getSpendById(this.expenseId).subscribe({
      next: (spend) => {
        if (!spend) {
          return;
        }
        this.expenseForm.patchValue({
          cuitConsorcio: spend.cuitConsorcio,
          cuitProveedor: spend.cuitProveedor,
          periodo: spend.periodo,
          tipoGasto: spend.tipoGasto,
          descripcion: spend.descripcion,
          monto: spend.monto,
          estadoPago: spend.estadoPago
        });
      },
      error: (error) => {
        console.error('Error loading expense:', error);
      }
    });
  }

  onFileDropped(file: File) {
    const allowed = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!allowed.includes(file.type)) {
      alert('Solo se permiten archivos JPG, PNG o PDF.');
      return;
    }
    this.selectedFile = file;
    this.fileName = file.name;
    this.isExtracting = true;
    this.spendsService.extractSpendFromFile(file)
      .pipe(finalize(() => {
        this.isExtracting = false;
      }))
      .subscribe({
        next: (response) => {
          const data = response?.data || {};
          this.applyExtractedData(data);
        },
        error: (error) => {
          console.error('Error al extraer datos del archivo:', error);
        }
      });
  }

  onFileRemove() {
    this.selectedFile = null;
    this.fileName = '';
    // El formulario permanece visible y no se resetea
  }

  onSubmit() {
    if (this.expenseForm.valid) {
      const formValue = this.expenseForm.value;
      const payload = {
        consorcio: formValue.cuitConsorcio,
        proveedor: formValue.cuitProveedor,
        periodo: formValue.periodo,
        descripcion: formValue.descripcion,
        monto: formValue.monto,
        tipo_gasto: formValue.tipoGasto,
        estado_pago: formValue.estadoPago
      };

      if (this.isEditMode && this.expenseId) {
        this.spendsService.updateSpend(this.expenseId, payload).subscribe({
          next: () => {
            this.router.navigate(['/dashboard', this.consortiumName, 'gastos']);
          },
          error: (error: any) => {
            console.error('Error al actualizar gasto:', error);
          }
        });
        return;
      }

      if (this.selectedFile) {
        this.spendsService.addSpendFromFile(payload, this.selectedFile).subscribe({
          next: () => {
            this.router.navigate(['/dashboard', this.consortiumName, 'gastos']);
          },
          error: (error: any) => {
            console.error('Error al cargar gasto desde archivo:', error);
          }
        });
        return;
      }

      this.spendsService.addSpend(payload).subscribe({
        next: () => {
          this.router.navigate(['/dashboard', this.consortiumName, 'gastos']);
        },
        error: (error: any) => {
          console.error('Error al agregar gasto:', error);
        }
      });
    } else {
      // Marcar todos los campos como touched para mostrar errores
      Object.keys(this.expenseForm.controls).forEach(key => {
        this.expenseForm.get(key)?.markAsTouched();
      });
    }
  }

  onCancel() {
    this.router.navigate(['/dashboard', this.consortiumName, 'gastos']);
  }

  private applyExtractedData(data: any) {
    const patch: any = {};

    if (data.cuit_proveedor) {
      patch.cuitProveedor = String(data.cuit_proveedor);
    }

    if (data.descripcion) {
      patch.descripcion = String(data.descripcion);
    }

    if (data.monto) {
      const montoStr = String(data.monto).replace(/\./g, '').replace(',', '.');
      const montoValue = Number(montoStr);
      if (!Number.isNaN(montoValue)) {
        patch.monto = montoValue;
      }
    }

    if (data.periodo) {
      const periodoValue = this.normalizePeriodo(String(data.periodo));
      if (periodoValue) {
        patch.periodo = periodoValue;
      }
    }

    this.expenseForm.patchValue(patch);
  }

  private normalizePeriodo(periodo: string): string | null {
    if (!periodo) {
      return null;
    }

    if (/^\d{4}-\d{2}-\d{2}$/.test(periodo)) {
      return periodo;
    }

    if (/^\d{2}\/\d{4}$/.test(periodo)) {
      const [month, year] = periodo.split('/');
      return `${year}-${month}-01`;
    }

    if (/^\d{2}\/\d{2}\/\d{4}$/.test(periodo)) {
      const [day, month, year] = periodo.split('/');
      return `${year}-${month}-${day}`;
    }

    return null;
  }
}