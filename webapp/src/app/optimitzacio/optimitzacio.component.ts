import {Component, OnInit} from '@angular/core';
import {MainService} from "../main-service/main.service";
import {saveAs} from 'file-saver';
import {LocalStorageService} from "../local-service/main.service";
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {valueOrDefault} from 'chart.js/dist/helpers/helpers.core';

@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './optimitzacio.component.html',
  styleUrls: ['./optimitzacio.component.css']
})
export class OptimitzacioComponent implements OnInit {

  loading: number = 0;
  formGroup: FormGroup;
  costTotal : number;


  constructor(
    private mainService: MainService,
    private localStorageService: LocalStorageService,
    private formBuilder: FormBuilder
  ) {
    this.formGroup = this.formBuilder.group({
      capacitat: ['', Validators.required],
      consum: ['', Validators.required],
      bombeig: ['', Validators.required]
    })
  }

  prediccioFeta : boolean = false;
  optimitzacioRebuda : any;
  loadingOptimitzacio : number = 0;

  ultimaPrediccio: { data: any, dia: Date }

  ngOnInit() {
    this.ultimaPrediccio = this.localStorageService.getLastPrediction();
  }

  generaExcel() {
    this.loading--;
    this.mainService.generaExcel(this.ultimaPrediccio.data).subscribe((response: Blob) => {
      const blob = new Blob([response], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
      saveAs(blob, 'prediccio.xlsx');
      this.loading++;
    })
  }

  generaExcelOptim(){
        this.loading--;
        console.log(this.optimitzacioRebuda)
    this.mainService.generaExcelOptimitzacio(this.optimitzacioRebuda).subscribe((response: Blob) => {
      const blob = new Blob([response], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
      saveAs(blob, 'optimitzacio.xlsx');
      this.loading++;
    })
  }

  capacitatTotal : number = 1;
  enviaForm() {
    this.formGroup.markAllAsTouched();
    if (this.formGroup.valid) {
      this.capacitatTotal = this.formGroup.get("capacitat").value;
      this.loadingOptimitzacio--;
      this.mainService.optimitza(this.ultimaPrediccio.data,
        this.formGroup.get("capacitat").value,
        this.formGroup.get("consum").value,
        this.formGroup.get("bombeig").value).subscribe((optimitzacio : any) => {
          this.loadingOptimitzacio++;
        this.prediccioFeta = true;
        this.optimitzacioRebuda = optimitzacio.llista
        this.costTotal = optimitzacio.total
      })
    }

  }

}
