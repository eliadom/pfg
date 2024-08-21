import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";


const headerDict = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Origin': '*'
}

const headerDictPost = {
  "Content-Type": "undefined",
  'Accept': 'application/json',
  'Access-Control-Allow-Headers': 'Content-Type',
}

const requestOptions = {
  headers: new Headers(headerDict),
};

const requestOptionsPost = {
  headers: new Headers(headerDictPost),
};

@Injectable({
  providedIn: 'root'
})

export class MainService {

  url: string = "/api"

  pujantModel: EventEmitter<boolean> = new EventEmitter();
  pujantModelActual: boolean;

  constructor(
    private http: HttpClient
  ) {
  }

  setPujantModel(what: boolean) {
    this.pujantModelActual = what;
    this.pujantModel.emit(this.pujantModelActual);
  }

  getPujantModelActual(): boolean {
    return this.pujantModelActual;
  }

  getPujantModel() {
    return this.pujantModel;
  }


  getTest(): any {
    // @ts-ignore
    // @ts-ignore
    // @ts-ignore
    return this.http.get<any>(this.url, requestOptions);
  }

  generaDeDies(dies: number): any {
    return this.http.get<any>(this.url + '/prediccio/' + dies);
  }

  generaExcel(array: any): any {
    return this.http.post<any>(this.url + '/excel', array, { responseType: 'blob' as 'json' });
  }


  demanaPreu(): any {
    return this.http.get<any>(this.url + '/getPreus');
  }

  optimitza(consumIData : any, capacitat : number, consum: number, bombeig: number){
    return this.http.post<any>(this.url + '/optimitzacio', {
      data_i_consum: consumIData,
      capacitat: capacitat,
      consum: consum,
      bombeig: bombeig
    }, { headers : headerDict});
  }

  getModels(): any {
    return this.http.get<any>(this.url + '/models');
  }

  getSeleccionat(): any {
    return this.http.get<any>(this.url + '/seleccionat/');
  }

  setSeleccionat(id: number) {
    return this.http.post<any>(this.url + '/seleccionat/' + id, null);
  }

  uploadFile(file: any) {
    const formData = new FormData();
    formData.append('file', file);
    // formData.append('some', "hola");
    console.log(formData)
    return this.http.post<any>(this.url + '/models/', formData);
  }


}
