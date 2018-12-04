import React, { Component } from 'react'
import { Button, FormControl, Row, Col } from 'react-bootstrap'

export default class WateringControl extends Component {

  render() {
    return (
      <div>
        <h3>Watering control</h3>
        <p>Pumping status: {(this.props.pumpingStatus) ? 'active' : 'deactive'}</p>
        <p>Speed:</p>
        <Row>
          <Col xs={6}>
            Speed
            <FormControl
              type="number"
              value={this.props.speed}
              onChange={this.props.changeSpeed}
            >
            </FormControl>
          </Col>
          <Col xs={6}>
            Time (seconds)
            <FormControl
              type="number"
              value={this.props.duration}
              onChange={this.props.changeDuration}
            >
            </FormControl>
          </Col>
        </Row>

        <Button bsStyle={this.props.pumpingStatus ? 'danger' : 'primary'} disabled={this.props.pumpingStatus} onClick={this.props.pump}>{this.props.pumpingStatus ? "Stop" : "Start"}</Button>
      </div>
    )
  }
}