import {Component} from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  template: `
    <div style="text-align:center">
      <h1>Exams</h1>
      <title>Frontend</title>
    </div>
    <h2>Here are the exams created so far: </h2>
    <router-outlet></router-outlet>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Frontend';
 }