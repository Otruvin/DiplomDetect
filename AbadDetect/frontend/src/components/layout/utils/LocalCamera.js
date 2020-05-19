import React, { Component, Fragment } from 'react';
import { connect, useSelector, useDispatch } from 'react-redux';
import Webcam from 'react-webcam';
import axios from 'axios';
import { getCameras } from '../../../actions/cameras';

const videoConstraints = {
  width: 480,
  height: 480,
  facingMode: "user"
};

const LocalCamera = () => {

  const [link, setLink] = React.useState('');

  const cameras = useSelector(state => state.cameras.cameras);
  const dispatch = useDispatch();

  const headers = {
    'Content-Type': 'application/json',
  };
     
  const webcamRef = React.useRef(null);
  
  const capture = React.useCallback(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
      axios.post('/detector/detectFrame/', {'background': imageSrc}, {
        headers: headers
      })
      .then((response) => {
        setLink(link => link = 'data:image/webp;base64,' + response.data['recieveData'])
      })
    },
    [webcamRef]
  );

  /*React.useEffect(() => {
    const interval = setInterval(() => {
      const imageSrc = webcamRef.current.getScreenshot();
      axios.post('/detector/detectFrame/', {'encodedFrame': imageSrc}, {
        headers: headers
      })
      .then((response) => {
        if(response)
        {
          setLink(link => link = 'data:image/webp;base64,' + response.data['recieveData'])
        }
      })
    }, 100);
    return () => clearInterval(interval);
  }, [webcamRef]);*/

  return (
    <Fragment>
      <h2>All Cameras</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Vide from local camera</th>
            <th>Video from detector</th>
          </tr>
        </thead>
        <tbody>
          { cameras.map(camera => (
            <tr key={camera.id}>
              <td>
                <h3>{camera.name_camera}</h3>
                <Webcam
                  audio={false}
                  height={480}
                  ref={webcamRef}
                  width={480}
                  videoConstraints={videoConstraints}
                />
                <button onClick={capture} className="btn btn-primary btn-sm">Capture background</button>
              </td>
              <td>
                <h3>Devise label</h3>
                <img src={link} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Fragment>
  );
};

const mapStateToProps = state => ({
  cameras: state.cameras.cameras
});

const mapDispatchToProps = { getCameras };

export default connect(mapStateToProps, mapDispatchToProps)(LocalCamera);
