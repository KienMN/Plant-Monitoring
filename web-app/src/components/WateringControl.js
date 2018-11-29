import React, { Component } from 'react'
import { Button, FormControl } from 'react-bootstrap'

export default class WateringControl extends Component {

  render() {
    return (
      <div>
        <h3>Watering control</h3>
        <p>Pumping status: {(this.props.pumpingStatus) ? 'active' : 'deactive'}</p>
        <p>Speed:</p>
        <FormControl
          type="number"
          value={this.props.speed}
          onChange={this.props.changeSpeed}
        >
        </FormControl>
        <Button bsStyle={this.props.pumpingStatus?'danger':'primary'} onClick={this.props.pump}>{this.props.pumpingStatus?"Stop":"Start"}</Button>
      </div>
    )
  }
}