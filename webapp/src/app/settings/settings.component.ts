import {Component, OnInit} from '@angular/core';
import {pipe} from "rxjs";
import {MainService} from "../main-service/main.service";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  chosenFile: boolean = false;
  fileName: string = null;

  constructor(
    private mainService: MainService,
    private _snackBar: MatSnackBar
  ) {
  }

  pujantModel : boolean = false;
  result: string = "";

  ngOnInit() {

    this.pujantModel = this.mainService.getPujantModelActual();

    this.mainService.getPujantModel().subscribe((what: boolean) => {
      this.pujantModel = what;
    })

    this.mainService.getTest().subscribe((test: any) => {
      this.result = test;
      console.log("service recibe:")
      console.log(this.result)
    })
  }


  onFileSelected(event) {

    const file: File = event.target.files[0];

    if (file) {
      this.chosenFile = true;
      this.fileName = file.name;
      const formData = new FormData();
      formData.append("thumbnail", file);
      this.mainService.setPujantModel(true);
      this.mainService.uploadFile(file).subscribe((res: any) => {
        this.mainService.setPujantModel(false);
        this._snackBar.open("Model penjat correctament!","OK",{
          duration: 5000
        });
      })
      // const upload$ = this.http.post("/api/thumbnail-upload", formData);
      // upload$.subscribe();
    }
  }

}
