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

  preus = []

  retornaPreus() {
    this.mainService.demanaPreu().subscribe((preus: any) => {
      console.log("preus:")
      console.log(preus)
      this.preus = preus;
    })
  }

  ultimaPrediccio: { data: any, dia: Date }

  ngOnInit() {
    this.retornaPreus()
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

  enviaForm() {
    this.formGroup.markAllAsTouched();
    console.log(this.formGroup.value)
    if (this.formGroup.valid) {
      // envia info a backend i fes optimitzacio...
    }

  }

}
