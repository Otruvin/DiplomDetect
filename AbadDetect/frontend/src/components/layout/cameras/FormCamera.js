import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { addCamera } from '../../../actions/cameras';
import Webcam from 'react-webcam';
import Select from 'react-select';

export class FormCamera extends Component {
    state = {
        min_area: '',
        max_area: '',
        time_to_detected: '',
        time_to_warn: '',
        time_to_forget: '',
        biggest_size: '',
        distance_to_undetect: '',
        name_camera: '',
        url_camera: '',
        local_connect: true,
        addCameraForm: false,
    };

    static propTypes = {
        addCamera: PropTypes.func.isRequired,
    };

    onAddCameraButtonClick = (e) => {
        this.setState({
            addCameraForm: !this.state.addCameraForm
        });
        
    }

    onChange = (e) => this.setState({ [e.target.name]: e.target.value});

    onChangelocal = (e) => {
        this.setState({
            local_connect: !this.state.local_connect
        })
    }

    handleLocalSelector = (selected) => {
        this.setState({
            url_camera: selected.value
        })
    }

    onSubmit = (e) => {
        e.preventDefault();
        const { min_area, max_area, time_to_detected, 
            time_to_warn, time_to_forget, biggest_size,
            distance_to_undetect, name_camera, url_camera, local_connect } = this.state;

        const camera = { min_area, max_area, time_to_detected,
            time_to_warn, time_to_forget, biggest_size,
            distance_to_undetect, name_camera, url_camera, local_connect };

        this.props.addCamera(camera);
        this.setState({
            min_area: '',
            max_area: '',
            time_to_detected: '',
            time_to_warn: '',
            time_to_forget: '',
            biggest_size: '',
            distance_to_undetect: '',
            name_camera: '',
            url_camera: '',
            local_connect: true,
            addCameraForm: false
        });
    };

    render() {
        const { min_area, max_area, time_to_detected, 
            time_to_warn, time_to_forget, biggest_size,
            distance_to_undetect, name_camera, url_camera,} = this.state;

        let devices = [];

        if (this.state.addCameraForm && this.state.local_connect)
        {
            navigator.mediaDevices.enumerateDevices().then( function(mdevices) {
                mdevices.filter(({ kind }) => kind === "videoinput").forEach( device => {
                    devices.push( { value: device.label, label: device.label } );
                })
            }); 
            
        }

        return (
            <div>
                {
                    this.state.addCameraForm?
                    <form onSubmit={this.onSubmit}>
                        <h2>Add new camera</h2>
                        <div className="form-row">
                            <div className="col">
                                <label for="minar">Min area</label>
                                <input type="number" name="min_area" className="form-control" id="minar" onChange={this.onChange} value={min_area} required/>
                                <label for="maxar">Max area</label>
                                <input type="number" name="max_area" className="form-control" id="maxar" onChange={this.onChange} value={max_area} required/>
                                <label for="td">Detect time</label>
                                <input type="number" name="time_to_detected" className="form-control" id="td" onChange={this.onChange} value={time_to_detected} required/>
                                <label for="tw">Warn time</label>
                                <input type="number" name="time_to_warn" className="form-control" id="tw" onChange={this.onChange} value={time_to_warn} required/>
                                <label for="tf">Forget time</label>
                                <input type="number" name="time_to_forget" className="form-control" id="tf" onChange={this.onChange} value={time_to_forget} required/>
                                <button type="submit" className="btn btn-success mt-3 mb-3">+Add new camera</button>
                            </div>
                            <div className="col">
                                <label for="bs">Human size</label>
                                <input type="number" name="biggest_size" className="form-control" id="bs" onChange={this.onChange} value={biggest_size} required/>
                                <label for="du">Undetect distance</label>
                                <input type="number" name="distance_to_undetect" className="form-control" id="du" onChange={this.onChange} value={distance_to_undetect} required/>
                                <label for="nc">Camera name</label>
                                <input type="text" name="name_camera" className="form-control" id="nc" onChange={this.onChange} value={name_camera} required/>
                                {
                                    this.state.local_connect?
                                    <div>
                                        <label for="locurl">Label of connected device</label>
                                        <Select onChange={this.handleLocalSelector} options={devices}/>
                                    </div>:
                                    <div>
                                        <label for="uc">Url camera</label>
                                        <input type="text" name="url_camera" className="form-control" id="uc" onChange={this.onChange} value={url_camera} required/>
                                    </div>
                                }
                                <label for="local">Device is local</label>
                                <input type="checkbox" checked={this.state.local_connect} id="local" onChange={this.onChangelocal}/>
                            </div>
                        </div>
                    </form>:
                    null
                }
                <button onClick={() => this.onAddCameraButtonClick()} className="btn btn-primary mt-3 mb-3">Add new camera</button>
            </div>
            
        );
    }
}

export default connect(null, { addCamera })(FormCamera);
