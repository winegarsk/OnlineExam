
import {Component, Inject, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {Exam} from './exam.model';
import {ExamsApiService} from './exams-api.service';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';
import { AppComponent } from '../app.component';

@Component({
  selector: 'exams',
  templateUrl: './exams.component.html',
  styleUrls: ['../app.component.css']
})
export class ExamsComponent implements OnInit, OnDestroy {
  examsListSubs!: Subscription|undefined;
  examsList: Exam[]|undefined;
  authenticated = false;

  constructor(@Inject(DOCUMENT) public document: Document, private examsApi: ExamsApiService,public auth: AuthService) { }

 

  ngOnInit() {
    this.examsListSubs = this.examsApi
      .getExams()
      .subscribe(res => {
          this.examsList = res;
        },
        console.error
      );
    const self = this;
  
  }

  ngOnDestroy() {
    this.examsListSubs!.unsubscribe();
  }
}