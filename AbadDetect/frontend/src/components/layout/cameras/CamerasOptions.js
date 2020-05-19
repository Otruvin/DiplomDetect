import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import {getCameras, deleteCamera, updateCamera} from '../../../actions/cameras';

export class CamerasOptions extends Component {

    static propTypes = {
        cameras: PropTypes.array.isRequired,
        getCameras: PropTypes.func.isRequired,
        deleteCamera: PropTypes.func.isRequired,
        updateCamera: PropTypes.func.isRequired,
    };

    state ={
        id: '',
        name_camera: '',
        min_area: '',
        max_area: '',
        time_to_detected: '',
        time_to_warn: '',
        time_to_forget: '',
        biggest_size: '',
        distance_to_undetect: '',
        url_camera: '',
        updateForm: false,
    }

    onChange = (e) => this.setState({ [e.target.name]: e.target.value });

    onUpdateClick = (camera) => {

        this.setState({
            id: camera.id,
            name_camera: camera.name_camera,
            min_area: camera.min_area,
            max_area: camera.max_area,
            time_to_detected: camera.time_to_detected,
            time_to_warn: camera.time_to_warn,
            time_to_forget: camera.time_to_forget,
            biggest_size: camera.biggest_size,
            distance_to_undetect: camera.distance_to_undetect,
            url_camera: camera.url_camera,
            updateForm: !this.state.updateForm
        });
    };

    onSubmit = (e) => {

        e.preventDefault();

        const { id, name_camera, min_area, max_area,
            time_to_detected, time_to_warn, time_to_forget,
            biggest_size, distance_to_undetect, url_camera } = this.state;

        const camera = { id, name_camera, min_area, max_area, time_to_detected,
            time_to_warn, time_to_forget, biggest_size, distance_to_undetect, url_camera };

        this.props.updateCamera(camera);

        this.setState({
            id: '',
            name_camera: '',
            min_area: '',
            max_area: '',
            time_to_detected: '',
            time_to_warn: '',
            time_to_forget: '',
            biggest_size: '',
            distance_to_undetect: '',
            url_camera: '',
            updateForm: false,
        })
    }

    componentDidMount() {
        this.props.getCameras();
    }

    
    render() {

        const { name_camera, min_area, max_area, time_to_detected, time_to_warn,
            time_to_forget, biggest_size, distance_to_undetect, url_camera } = this.state;

        return (
            <Fragment>
                {

                    this.state.updateForm?
                    <form className="mb-3" onSubmit={this.onSubmit}>
                        <h2>Update {name_camera}</h2>
                        <div className="row">
                            <div className="col">
                                <input type="text" name="name_camera" onChange={this.onChange} value={name_camera} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="min_area" onChange={this.onChange} value={min_area} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="max_area" onChange={this.onChange} value={max_area} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="time_to_detected" onChange={this.onChange} value={time_to_detected} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="time_to_warn" onChange={this.onChange} value={time_to_warn} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="time_to_forget" onChange={this.onChange} value={time_to_forget} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="biggest_size" onChange={this.onChange} value={biggest_size} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="number" name="distance_to_undetect" onChange={this.onChange} value={distance_to_undetect} className="form-control" />
                            </div>
                            <div className="col">
                                <input type="text" name="url_camera" onChange={this.onChange} value={url_camera} className="form-control" />
                            </div>
                            <button type="submit" className="btn btn-success ml-3">Update</button>
                        </div>
                    </form>:
                    null
                }
                <h2>User's cameras</h2>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>name</th>
                            <th>min area (px)</th>
                            <th>max area (px)</th>
                            <th>detect time (ms)</th>
                            <th>warn time (ms)</th>
                            <th>forget time (ms)</th>
                            <th>human size (px)</th>
                            <th>undetect distance (px)</th>
                            <th>url camera</th>
                        </tr>
                    </thead>
                    <tbody>
                        { this.props.cameras.map(camera => (
                            <tr key={camera.id}>
                                <td>{camera.name_camera}</td>
                                <td>{camera.min_area}</td>
                                <td>{camera.max_area}</td>
                                <td>{camera.time_to_detected}</td>
                                <td>{camera.time_to_warn}</td>
                                <td>{camera.time_to_forget}</td>
                                <td>{camera.biggest_size}</td>
                                <td>{camera.distance_to_undetect}</td>
                                <td>{camera.url_camera}</td>
                                <td><button onClick={this.props.deleteCamera.bind(this, camera.id)} className="btn btn-danger btn-sm">Delete</button></td>
                                <td><button onClick={() => this.onUpdateClick(camera)} className="btn btn-warning">Update</button></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </Fragment>
        );
    }

}

/*

*/

const mapStateToProps = state => ({
    cameras: state.cameras.cameras,
});

export default connect(mapStateToProps, { getCameras, deleteCamera, updateCamera})(CamerasOptions)
