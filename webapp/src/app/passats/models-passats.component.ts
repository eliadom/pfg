import {Component, OnInit} from '@angular/core';
import {MainService} from "../main-service/main.service";

@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './models-passats.component.html',
  styleUrls: ['./models-passats.component.css']
})
export class ModelsPassatsComponent implements OnInit {
  title = 'webapp';

  constructor(
    private mainService : MainService
  ){}
  result : string = "";
  ngOnInit() {
    this.mainService.getTest().subscribe((test : any) => {
      this.result = test;
      console.log("service recibe:")
      console.log(this.result)
    })
  }
}
