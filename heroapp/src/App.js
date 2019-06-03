import * as React from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';

import InputForm from './components/InputForm';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import DisplayTable from './components/DisplayTable';

class App extends React.Component {
  render() {
    return (
      <Router>
        <nav className="navbar navbar-dark bg-dark">
          <span className="navbar-brand mb-0 h1">Hero Form</span>
        </nav>

        <Switch>
          <Route path="/display" exact component={DisplayTable} />
          <Route component={InputForm} />
        </Switch>
      </Router>
    );
  }
}

export default App;
