import {Component, OnInit} from '@angular/core';
import {pipe} from "rxjs";
import {MainService} from "../main-service/main.service";

@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
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
