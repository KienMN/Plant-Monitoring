import React, { Component } from 'react'
import { Button } from 'react-bootstrap'

export default class WateringControl extends Component {

  render() {
    return (
      <div>
        <h3>Watering control</h3>
        <p>Pumping status: {(this.props.pumpingStatus) ? 'active' : 'deactive'}</p>
        <Button bsStyle={this.props.pumpingStatus?'danger':'primary'} onClick={this.props.pump}>{this.props.pumpingStatus?"Stop":"Start"}</Button>
      </div>
    )
  }
}