import React, {Component} from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

import logo from './logo.svg';
import './App.css';

import Register from './components/Register/Register';

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

    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact path="/register" component={ Register } />
                    {/* <Route exact path="/login" component={ Login } /> */}
                    {/* <Route path="/" component={ RedirectToLogin } /> */}
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;
