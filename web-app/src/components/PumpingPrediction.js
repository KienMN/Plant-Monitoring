import React, { Component } from 'react'

export default class PumpingPrediction extends Component {

  render() {
    return (
      <div>
        <h3>Pumping time prediction</h3>
        <p>Predicted time: {this.props.predictedTime}</p>
        <p>Predicted duration: {this.props.predictedDuration}</p>
      </div>
    )
  }
}