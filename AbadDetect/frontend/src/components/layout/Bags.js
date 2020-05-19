import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getBags, deleteBag } from '../../actions/bags';

export class Bags extends Component {
    static propTypes = {
        bags: PropTypes.array.isRequired
    };

    componentDidMount() {
        this.props.getBags();
    }

    render() {
        return (
            <Fragment>
                <h2>Abad objects</h2>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>date_detect</th>
                            <th>Image</th>
                            <th>coord_x</th>
                            <th>coord_y</th>
                            <th/>
                        </tr>
                    </thead>
                    <tbody>
                        { this.props.bags.map(bag => (
                            <tr key={bag.id}>
                                <td>{bag.date_detect}</td>
                                <td><img src={bag.link_to_image} width="50" height="50"/></td>
                                <td>{bag.coord_x}</td>
                                <td>{bag.coord_y}</td>
                                <td><button onClick={this.props.deleteBag.bind(this, bag.id)} className="btn btn-danger btn-sm">Delete</button></td>
                            </tr>
                        )) }
                    </tbody>
                </table>
            </Fragment>
        );
    }
}

const mapStateToProps = state => ({
    bags: state.bags.bags
});

export default connect(mapStateToProps, { getBags, deleteBag })(Bags);