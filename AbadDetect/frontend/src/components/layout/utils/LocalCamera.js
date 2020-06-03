import React, { Component, Fragment } from 'react';
import { connect, useSelector, useDispatch } from 'react-redux';
import Webcam from 'react-webcam';
import axios from 'axios';
import { getCameras } from '../../../actions/cameras';

const videoConstraints = {
  width: 480,
  height: 480,
  facingMode: "user",
  deviceId: 1
};

const LocalCamera = () => {

  const [link, setLink] = React.useState('');
  const [deviceId, setDeviceId] = React.useState({});
  const [devices, setDevices] = React.useState([]);
  const [addedCameras, setAddedCameras] = React.useState(false);

  const cameras = useSelector(state => state.cameras.cameras);
  const dispatch = useDispatch();

  const headers = {
    'Content-Type': 'application/json',
  };
     
  const webcamRef = React.useRef(null);
  

  const handleDevices = React.useCallback(
    mediaDevices => 
      setDevices(mediaDevices.filter(({ kind }) => kind === "videoinput")),
      [setDevices]
  );


  const updateBackground = (camera) => {
    const imageSrc = webcamRef.current.getScreenshot();
    axios.post('/detector/getBack/', { 'encodedFrame' : imageSrc, 'idCam': camera}, {
      headers: headers
    })
    .then((response) => {
      if (response)
      {
        console.log(response)
      }
    })
  }

  React.useEffect(
    () => {
      if (!addedCameras && cameras != [])
      {
        navigator.mediaDevices.enumerateDevices().then(handleDevices);
        console.log(cameras);
        axios.post('/detector/createDetectors/', cameras, {
          headers: headers
        })
        .then((response) => {
          console.log(response)
          setAddedCameras(true)
        })
      }
    },
    [handleDevices, cameras]
  );

  React.useEffect(() => {
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
    }, 300);
    return () => clearInterval(interval);
  }, [webcamRef]);

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
            {
              devices.forEach( device => {
                if ( device.label === camera.url_camera)
                {
                  videoConstraints.deviceId = device.deviceId
                }
              })
            }
              <td>
                <h3>{camera.name_camera}</h3>
                <Webcam
                  audio={false}
                  height={480}
                  ref={webcamRef}
                  width={480}
                  videoConstraints={videoConstraints}
                />
                <button onClick={() => updateBackground(camera.id)} className="btn btn-primary btn-sm">Capture background</button>
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
