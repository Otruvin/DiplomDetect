import React, { Fragment } from 'react';
import FormCamera from './FormCamera';
import CamerasOptions from './CamerasOptions';

//<FormCamera />

export default function CamerasWindow() {
    return (
        <Fragment>
            <FormCamera />
            <CamerasOptions />
        </Fragment>
    );
}

