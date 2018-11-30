import React, { Component } from 'react'
import { Button, FormControl } from 'react-bootstrap'

export default class PumpingPrediction extends Component {

  render() {
    return (
      <div>
        <h3>Pumping time prediction</h3>
        <p>Predicted time: {this.props.predictedTime}</p>
        <p>Predicted duration: {this.props.predictedDuration}</p>
        {/* <FormControl
          type="number"
          value={this.props.speed}
          onChange={this.props.changeSpeed}
        >
        </FormControl> */}
        {/* <Button bsStyle={this.props.pumpingStatus?'danger':'primary'} onClick={this.props.pump}>{this.props.pumpingStatus?"Stop":"Start"}</Button> */}
      </div>
    )
  }
}