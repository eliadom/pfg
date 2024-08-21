import {Component, OnInit} from '@angular/core';
import {MainService} from "../main-service/main.service";
import {IAModel} from "../model/ia_mod/ia_mod";

@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './models-passats.component.html',
  styleUrls: ['./models-passats.component.css']
})
export class ModelsPassatsComponent implements OnInit {
  title = 'webapp';
  models: IAModel[];
  loading: number = 0;

  pujantModel: boolean = false;
  seleccionat: number = -1;

  constructor(
    private mainService: MainService
  ) {
  }

  ngOnInit() {

    this.pujantModel = this.mainService.getPujantModelActual();

    this.mainService.getPujantModel().subscribe((what: boolean) => {
      this.pujantModel = what;
    })

    this.loading--;
    this.mainService.getModels().subscribe((models) => {
      console.log("rebut:")
      console.log(models)
      this.models = models;
      this.loading++;
    })

    this.mainService.getSeleccionat().subscribe((resul: any) => {
      this.seleccionat = resul.id;
    })
  }

  marcaSeleccionat(numb: number) {
    this.mainService.setSeleccionat(numb).subscribe((resul: any) => {
      this.seleccionat = resul.id;
    });
  }
}
