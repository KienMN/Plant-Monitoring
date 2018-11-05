import React, { Component } from 'react';
import ReactSpeedometer from 'react-d3-speedometer'
import { Row, Col } from 'react-bootstrap'

class ParametersDisplay extends Component {

  render() {
    return (
      <div>
        <h3>Parameters</h3>
        <Row>
          <Col md={3} sm={6} xs={12}>
            <p>Temperature</p>
            <ReactSpeedometer value={this.props.temperature} minValue={-50} maxValue={50} startColor="#ff471a" endColor="#ff471a" height={200}/>
          </Col>
          <Col md={3} sm={6} xs={12}>
            <p>Humidity</p>
            <ReactSpeedometer value={this.props.humidity} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" height={200}/>
          </Col>
          <Col md={3} sm={6} xs={12}>
            <p>Soil moisture</p>
            <ReactSpeedometer value={this.props.soilMoisture} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" height={200}/>
          </Col>
          <Col md={3} sm={6} xs={12}>
            <p>Light intensity</p>
            <ReactSpeedometer value={this.props.lightIntensity} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" height={200}/>
          </Col>
        </Row>
      </div>
    )
  }
}

export default ParametersDisplay