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
  models : IAModel[];
  loading : number = 0;

  constructor(
    private mainService : MainService
  ){}
  ngOnInit() {
    this.loading--;
    this.mainService.getModels().subscribe((models : IAModel[]) => {
      this.models = models;
      this.loading++;
    })
  }


}
