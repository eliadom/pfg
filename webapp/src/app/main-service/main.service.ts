import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";


const headerDict = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Access-Control-Allow-Headers': 'Content-Type',
}

const requestOptions = {
  headers: new Headers(headerDict),
};
@Injectable({
  providedIn: 'root'
})

export class MainService {

  url : string = "/api"

  constructor(
    private http : HttpClient
  ) { }

    getTest() : any {
    // @ts-ignore
      // @ts-ignore
      // @ts-ignore
      return this.http.get<any>(this.url, requestOptions);
  }

}
