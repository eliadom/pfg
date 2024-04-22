import {Component, OnInit} from '@angular/core';
import {pipe} from "rxjs";
import {MainService} from "../main-service/main.service";

@Component({
  selector: 'app-taula-prediccions',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  chosenFile: boolean = false;
  fileName: string = null;

  constructor(
    private mainService: MainService
  ) {
  }

  result: string = "";

  ngOnInit() {
    this.mainService.getTest().subscribe((test: any) => {
      this.result = test;
      console.log("service recibe:")
      console.log(this.result)
    })
  }


  onFileSelected(event) {
    console.log("SELECTED A FILE")

    const file: File = event.target.files[0];

    if (file) {
      console.log("DETECTED FILE!!")
      this.chosenFile = true;
      this.fileName = file.name;

      const formData = new FormData();

      formData.append("thumbnail", file);

      console.log("event:")
      console.log(file)


      this.mainService.uploadFile(file).subscribe((res : any) => {
        console.log("done!")
        console.log(res)
      })
      // const upload$ = this.http.post("/api/thumbnail-upload", formData);
      // upload$.subscribe();
    }
  }

}
