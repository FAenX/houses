import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom'
import { Route, Link } from 'react-router-dom'

import  ManagersList from './ManagersList'
import  ManagerCreateUpdate  from './ManagerCreateUpdate'
import './App.css';

const BaseLayout = () => (
  <div className="container-fluid">
<nav className="navbar navbar-expand-lg navbar-light bg-light">
  <a className="navbar-brand" href="#">Django React Demo</a>
  <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span className="navbar-toggler-icon"></span>
  </button>
  <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div className="navbar-nav">
      <a className="nav-item nav-link" href="/">CUSTOMERS</a>
      <a className="nav-item nav-link" href="/manager">CREATE CUSTOMER</a>

    </div>
  </div>
</nav>  

    <div className="content">
      <Route path="/" exact component={ManagersList} />
      <Route path="/manager/:pk"  component={ManagerCreateUpdate} />
      <Route path="/manager/" exact component={ManagerCreateUpdate} />

    </div>

  </div>
)

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <BaseLayout/>
      </BrowserRouter>
    );
  }
}

export default App;
