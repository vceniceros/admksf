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

  constructor(
    private fb: FormBuilder,
    private spendsService: SpendsService,
    private router: Router,
    private route: ActivatedRoute
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
    });
  }

  onFileDropped(file: File) {
    this.selectedFile = file;
    this.fileName = file.name;
    // Por ahora no procesamos con OCR, solo guardamos la referencia del archivo
  }

  onFileRemove() {
    this.selectedFile = null;
    this.fileName = '';
    // El formulario permanece visible y no se resetea
  }

  onSubmit() {
    if (this.expenseForm.valid) {
      const formValue = this.expenseForm.value;
      const newSpend = {
        idGasto: Date.now(),
        cuitConsorcio: formValue.cuitConsorcio,
        cuitProveedor: formValue.cuitProveedor,
        periodo: formValue.periodo,
        descripcion: formValue.descripcion,
        monto: formValue.monto,
        fechaRegistro: new Date().toISOString(),
        tipoGasto: formValue.tipoGasto,
        estadoPago: formValue.estadoPago
      };

      this.spendsService.addSpend(newSpend).subscribe({
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
}