import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {pipe} from "rxjs";
import {MainService} from "../main-service/main.service";
import {PrediccioModel} from "../model/prediccio/prediccio";
import {MatSort, Sort} from "@angular/material/sort";
import {MatTableDataSource} from "@angular/material/table";
import {LiveAnnouncer} from "@angular/cdk/a11y";


@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './taula-prediccions.component.html',
  styleUrls: ['./taula-prediccions.component.css']
})
export class TaulaPrediccionsComponent implements OnInit, AfterViewInit {
  title = 'webapp';
  displayedColumns = ['zona.nom', 'col1', 'col2', 'valorPrevist'];
  dataSource = new MatTableDataSource(prediccions);

  constructor(
    private mainService: MainService,
    private _liveAnnouncer: LiveAnnouncer
  ) {
  }


  result: string = "";
  loading : number = 0;


  @ViewChild(MatSort) sort: MatSort;

  ngAfterViewInit() {

    this.dataSource.sort = this.sort;
console.log(this.sort)
  }

  ngOnInit() {
this.dataSource.sortingDataAccessor = (item, property) => {
    switch(property) {
      case 'zona.nom': return item.zona.nom;
      default: return item[property];
    }
  };
  this.dataSource.sort = this.sort;
    // this.dataSource.sortingDataAccessor = (item, property) => {
    //   switch (property) {
    //     // case 'break': return item.break.start;
    //     default:
    //       return item[property];
    //   }
    // };
    this.loading--;
    this.mainService.getTest().subscribe((test: any) => {
      this.result = test;
      console.log("service recibe:")
      console.log(this.result)
      this.loading++;
    })
  }
}

// ---------------------------------------------------------------------------------------------------------------------

const prediccions = [{
  zona: {
    codi: 1,
    nom: "Zona A"
  },
  valorPrevist: 224.45
}, {
  zona: {
    codi: 2,
    nom: "Zona B"
  },
  valorPrevist: 22.23
},
  {
    zona: {
      codi: 3,
      nom: "Zona C"
    },
    valorPrevist: 19.29
  },
  {
    zona: {
      codi: 4,
      nom: "Zona D"
    },
    valorPrevist: 2.01
  },
  {
    zona: {
      codi: 5,
      nom: "Zona E"
    },
    valorPrevist: 0.34
  },
  {
    zona: {
      codi: 6,
      nom: "Zona F"
    },
    valorPrevist: 82.45
  },

]
