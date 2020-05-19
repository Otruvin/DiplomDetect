import React, { Component } from 'react';
import Webcam from 'react-webcam';
import { connect } from 'react-redux';
import LocalCamera from './utils/LocalCamera';

export class MainPage extends Component {

    render() {
        return (
            <LocalCamera />
        );
    }
}

export default MainPage
