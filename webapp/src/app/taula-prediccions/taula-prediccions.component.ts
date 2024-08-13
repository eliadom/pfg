import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {ChartConfiguration, ChartEvent, ChartType} from 'chart.js';
import {MainService} from "../main-service/main.service";
import {PrediccioModel} from "../model/prediccio/prediccio";
import {MatSort, Sort} from "@angular/material/sort";
import {MatTableDataSource} from "@angular/material/table";
import {LiveAnnouncer} from "@angular/cdk/a11y";
import { saveAs } from 'file-saver';
import {LocalStorageService} from "../local-service/main.service";


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
    private _liveAnnouncer: LiveAnnouncer,
    private localStorageService : LocalStorageService
  ) {
  }


  result: string = "";
  loading: number = 0;

  arrayDiaIHora: Date[] = [];


  @ViewChild(MatSort) sort: MatSort;

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  ngOnInit() {


    this.dataSource.sortingDataAccessor = (item, property) => {
      switch (property) {
        case 'zona.nom':
          return item.zona.nom;
        default:
          return item[property];
      }
    };
    this.dataSource.sort = this.sort;

  }

  public ChartType = 'bar';

  sliderValue: number = 1;
  loadedImage: boolean = false;
  imagePath;

  arrayData: number[] = [];
  arrayWithDate : consumIData[] = [];

  generaExcel() {
    this.loading--;
    this.mainService.generaExcel(this.arrayWithDate).subscribe((response: Blob) => {
       const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(blob, 'prediccio.xlsx');
      this.loading++;
    })
  }

  generaPrediccioDe() {

    let dateNow: Date = new Date();
    for (let i = 0; i < this.sliderValue; i++) {
      for (let j = 0; j < 24; j++) {
        dateNow.setTime(dateNow.getTime() + (1 * 60 * 60 * 1000));
        dateNow = new Date(dateNow)
        this.arrayDiaIHora.push(dateNow);
      }
    }

    console.log(this.arrayDiaIHora)

    this.loading--;
    this.mainService.generaDeDies(this.sliderValue).subscribe((test: any) => {
      this.loading++;
      // this.arrayData = test.resul;

      let i = 0;
      test.resul.forEach(numberReceived => {
        let retNumber: string = numberReceived.toString();
        let numberAgain: number = Number(retNumber.split(".")[0]);
        this.arrayData.push(numberAgain)
        this.arrayWithDate.push({
          data : this.arrayDiaIHora[i].toISOString().slice(0, -5),
          consum : numberAgain
        })
        i++;
      })
      console.log("arrayData:")
      console.log(this.arrayData)

            console.log("arrayWithDate:")
      console.log(this.arrayWithDate)

      this.localStorageService.setLastPrediction(this.arrayWithDate)

      this.arrayData.forEach(result => {
        this.lineChartData.labels.push('')
      })
      this.lineChartData.datasets.push(
        {
          data: this.arrayData,
          label: 'Predicció',
          backgroundColor: 'rgba(148,159,177,0.2)',
          borderColor: 'rgba(148,159,177,1)',
          pointBackgroundColor: 'rgba(148,159,177,1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(148,159,177,0.8)',
          fill: 'origin',
        }
      );
      this.loadedImage = true;
      // @ts-ignore
      document.getElementById('image').src = test.plot
    })
  }

  chartHovered($event
                 :
                 {
                   event?: ChartEvent;
                   active?: object[]
                 }
  ) {
    // console.log("hover")
  }

  chartClicked($event
                 :
                 {
                   event?: ChartEvent;
                   active?: object[]
                 }
  ) {
    // console.log("CLICKED")
  }


  public
  lineChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: [],
  };
  // labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],

  // @ts-ignore
  public
  lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    elements: {
      line: {
        tension: 0.5,
      },
    },
    scales: {
      // We use this empty structure as a placeholder for dynamic theming.
      y: {
        position: 'left',
      },
      y1: {
        position: 'right',
        grid: {
          color: 'rgba(255,0,0,0.3)',
        },
        ticks: {
          color: 'red',
        },
      },
    },

    plugins: {
      legend: {display: true},
      // @ts-ignore
      annotation: {
        annotations: [
          {
            type: 'line',
            scaleID: 'x',
            value: 'March',
            borderColor: 'orange',
            borderWidth: 2,
            label: {
              display: true,
              position: 'center',
              color: 'orange',
              content: 'LineAnno',
              font: {
                weight: 'bold',
              },
            },
          },
        ],
      },
    },
  };

  public lineChartType: ChartType = 'line';


}

class consumIData {
  consum : number;
  data : string
}

// ---------------------------------------------------------------------------------------------------------------------

const
  prediccions = [{
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
