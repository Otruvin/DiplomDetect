import React, { useEffect, useState, useRef, Fragment } from 'react';
import ReactDOM, { render } from 'react-dom';

import {Provider as AlertProvider} from 'react-alert';
import AlertTemplate from 'react-alert-template-basic';

import Header from './layout/Header';
import DashBoardBags from './layout/DashBoardBags';
import CamerasOpt from './layout/cameras/CamerasWindow';
import LocalCamera from './layout/utils/LocalCamera';
import Alerts from './layout/Alerts';
import Login from './accounts/Login';
import Register from './accounts/Register';
import Profile from './layout/Profile';
import PrivateRoute from './common/PrivateRoute';
import { HashRouter as Router, Route, Switch, Redirect } from "react-router-dom"

import { Provider, connect } from 'react-redux';
import store from '../store';
import { loadUser } from '../actions/auth';
import { getCameras } from '../actions/cameras'
import MainPage from './layout/MainPage';
import CamerasWindow from './layout/cameras/CamerasWindow';

const alertOptions = {
    timeout: 3000,
    position: 'top center'
};

class App extends React.Component
{
    componentDidMount() {
        store.dispatch(getCameras());
        //store.dispatch(loadUser());
    }
    render()
    {
        return (
            <Provider store={store}>
                <AlertProvider template={AlertTemplate} {...alertOptions}>
                    <Router>
                        <Fragment>
                            <Header />
                            <Alerts />
                            <div className="container">
                                <Switch>
                                    <PrivateRoute exact path="/" component= {MainPage} />
                                    <PrivateRoute exact path="/detected" component={DashBoardBags} />
                                    <PrivateRoute exact path="/cameras" component= {CamerasWindow} />
                                    <PrivateRoute exact path="/profile" component={Profile} />
                                    <Route exact path="/register" component= {Register} />
                                    <Route exact path="/login" component= {Login} />
                                </Switch>
                            </div>
                        </Fragment>
                    </Router>
                </AlertProvider>
            </Provider>
        )
    }
}

ReactDOM.render(<App/>, document.getElementById('app'));