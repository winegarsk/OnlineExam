import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {ExamsApiService} from './exams/exams-api.service';
import {Exam} from './exams/exam.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'frontend';
  examsListSubs: Subscription|undefined;
  examsList: Exam[]|undefined;

  constructor(private examsApi: ExamsApiService) {
    this.examsList = [];
    this.examsListSubs = this.examsApi .getExams()
    .subscribe(res => {
        this.examsList = res;
      },
      console.error
    ); ;
  }

  ngOnInit() {
    this.examsListSubs = this.examsApi
      .getExams()
      .subscribe(res => {
          this.examsList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this?.examsListSubs?.unsubscribe();
  }
}