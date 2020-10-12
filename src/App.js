import React, {Component} from 'react'
import {BrowserRouter, Route, Switch} from 'react-router-dom'

import logo from './logo.svg'
import './App.css'

import Main from './components/Main/Main'
import SignUp from './components/SignUp/SignUp'
import SignIn from './components/SignIn/SignIn'
import PasswordReset from './components/PasswordReset/PasswordReset'
import Discover from './components/Discover/Discover'

class App extends Component {
    // constructor(props) {
    //     super(props);
    //     this.state = {
    //
    //     };
    // }
    //
    // componentDidMount() {
    //
    // }

  render () {
    return (
      <BrowserRouter>
        <Switch>
          <Route exact path='/users/signup' component={SignUp} />
          <Route exact path='/users/signin' component={SignIn} />
          <Route exact path='/users/passwordreset' component={PasswordReset} />
          <Route exact path='/discover' component={Discover} />
          <Route exact path='/' component={Main} />
          {/* <Route path='/' component={RedirectToLogin} /> */}
        </Switch>
      </BrowserRouter>
    )
  }
}

export default App
