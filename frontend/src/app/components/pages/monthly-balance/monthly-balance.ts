import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MonthlyBalanceService } from '../../../services/monthly-balance.service';
import { ConsortiumService } from '../../../services/consortium.service';
import { MonthlyBalance } from '../../../../models/monthly-balance.model';
import { LabelComponent } from '../../atoms/label.component/label.component';
import { IconComponent } from '../../atoms/icon.component/icon.component';
import { MonthlyBalanceTableComponent } from '../../molecules/monthly-balance-table.component/monthly-balance-table.component';

@Component({
  selector: 'app-monthly-balance',
  imports: [CommonModule, ReactiveFormsModule, LabelComponent, IconComponent, MonthlyBalanceTableComponent],
  templateUrl: './monthly-balance.html',
  styleUrls: ['./monthly-balance.css'],
  standalone: true
})
export class MonthlyBalancePage implements OnInit {
  consortiumName: string = '';
  consortiumId: string = '';
  balances: MonthlyBalance[] = [];

  showFormModal = false;
  showDeleteModal = false;
  isEditMode = false;
  selectedBalance: MonthlyBalance | null = null;
  balanceToDelete: MonthlyBalance | null = null;
  form: FormGroup;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private monthlyBalanceService: MonthlyBalanceService,
    private consortiumService: ConsortiumService,
    private fb: FormBuilder
  ) {
    this.form = this.fb.group({
      numeroUnidad: ['', [Validators.required, Validators.min(1)]],
      consorcio: [{ value: '', disabled: true }, [Validators.required]],
      mesAnio: ['', Validators.required],
      saldoInicial: [0, [Validators.required, Validators.min(0)]],
      totalGastos: [0, [Validators.required, Validators.min(0)]],
      totalPagos: [0, [Validators.required, Validators.min(0)]],
      fechaCierre: ['']
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
          this.loadBalances();
        }
      },
      error: (error) => {
        console.error('Error loading consortium:', error);
      }
    });
  }

  loadBalances() {
    if (!this.consortiumId) {
      return;
    }
    this.monthlyBalanceService.getBalancesByConsortium(this.consortiumId).subscribe({
      next: (data) => {
        this.balances = data;
      },
      error: (error) => {
        console.error('Error loading monthly balances:', error);
      }
    });
  }

  openCreateModal() {
    this.isEditMode = false;
    this.selectedBalance = null;
    this.form.reset({
      numeroUnidad: '',
      consorcio: this.consortiumId,
      mesAnio: '',
      saldoInicial: 0,
      totalGastos: 0,
      totalPagos: 0,
      fechaCierre: ''
    });
    this.showFormModal = true;
  }

  openEditModal(balance: MonthlyBalance) {
    this.isEditMode = true;
    this.selectedBalance = balance;
    this.showFormModal = true;
    this.form.reset({
      numeroUnidad: balance.numeroUnidad,
      consorcio: balance.cuitConsorcio || this.consortiumId,
      mesAnio: balance.mesAnio,
      saldoInicial: balance.saldoInicial,
      totalGastos: balance.totalGastos,
      totalPagos: balance.totalPagos,
      fechaCierre: balance.fechaCierre ?? ''
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
      numero_de_unidad_funcional: Number(raw.numeroUnidad),
      consorcio: String(raw.consorcio ?? '').trim(),
      mes_anio: raw.mesAnio,
      saldo_inicial: raw.saldoInicial,
      total_gastos: raw.totalGastos,
      total_pagos: raw.totalPagos,
      fecha_cierre: raw.fechaCierre || null
    };

    if (this.isEditMode && this.selectedBalance) {
      this.monthlyBalanceService.updateBalance(this.selectedBalance.id, payload).subscribe({
        next: () => {
          this.closeFormModal();
          this.loadBalances();
        },
        error: (error) => {
          console.error('Error updating monthly balance:', error);
        }
      });
      return;
    }

    this.monthlyBalanceService.createBalance(payload).subscribe({
      next: () => {
        this.closeFormModal();
        this.loadBalances();
      },
      error: (error) => {
        console.error('Error creating monthly balance:', error);
      }
    });
  }

  onDeleteBalance(balance: MonthlyBalance) {
    this.balanceToDelete = balance;
    this.showDeleteModal = true;
  }

  closeDeleteModal() {
    this.showDeleteModal = false;
    this.balanceToDelete = null;
  }

  confirmDelete() {
    if (!this.balanceToDelete) {
      return;
    }
    this.monthlyBalanceService.deleteBalance(this.balanceToDelete.id).subscribe({
      next: () => {
        this.closeDeleteModal();
        this.loadBalances();
      },
      error: (error) => {
        console.error('Error deleting monthly balance:', error);
      }
    });
  }

  onAddPayment() {
    this.router.navigate(['/dashboard', this.consortiumName, 'pagos', 'carga-de-pago']);
  }
}
