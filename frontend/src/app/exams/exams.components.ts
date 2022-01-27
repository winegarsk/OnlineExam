
import {Component, Inject, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {Exam} from './exam.model';
import {ExamsApiService} from './exams-api.service';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'exams',
  template: `
    <div>
      <ul *ngIf="auth.user$ | async as user">
        <li>Hello {{ user.name }}</li>
      </ul>
      <button routerLink="/new-exam">New Exam</button>
      <ng-container *ngIf="auth.isAuthenticated$ | async; else loggedOut">
      <button (click)="auth.logout({ returnTo: document.location.origin })">
        Log out
      </button>
    </ng-container>

    <ng-template #loggedOut>
      <button (click)="auth.loginWithRedirect()">Log in</button>
    </ng-template>
      
      <ul>
        <li *ngFor="let exam of examsList">
          {{exam.title}}
        </li>
      </ul>
    </div>
  `
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