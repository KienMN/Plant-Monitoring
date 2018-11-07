import React, { Component } from 'react';
import ReactSpeedometer from 'react-d3-speedometer'
import { Row, Col, Panel } from 'react-bootstrap'

class ParametersDisplay extends Component {

  render() {
    return (
      <div>
        <h3>Parameters</h3>
        <Row>
          <Col md={3} sm={6} xs={12}>
            <Panel>
              <Panel.Heading>
                <Panel.Title>Temperature</Panel.Title>
              </Panel.Heading>
              <Panel.Body>
                <ReactSpeedometer value={this.props.temperature} minValue={-50} maxValue={50} startColor="#ff471a" endColor="#ff471a" height={200} />
              </Panel.Body>
            </Panel>
          </Col>
          <Col md={3} sm={6} xs={12}>
            <Panel>
              <Panel.Heading>
                <Panel.Title>Humidity</Panel.Title>
              </Panel.Heading>
              <Panel.Body>
                <ReactSpeedometer value={this.props.humidity} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" height={200} />
              </Panel.Body>
            </Panel>
          </Col>
          <Col md={3} sm={6} xs={12}>
            <Panel>
              <Panel.Heading>
                <Panel.Title>Soil moisture</Panel.Title>
              </Panel.Heading>
              <Panel.Body>
                <ReactSpeedometer value={this.props.soilMoisture} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" height={200} />
              </Panel.Body>
            </Panel>
          </Col>
          <Col md={3} sm={6} xs={12}>
            <Panel>
              <Panel.Heading>
                <Panel.Title>Light intensity</Panel.Title>
              </Panel.Heading>
              <Panel.Body>
                <ReactSpeedometer value={this.props.lightIntensity} minValue={0} maxValue={1024} startColor="#ff471a" endColor="#ff471a" height={200} />
              </Panel.Body>
            </Panel>
          </Col>
        </Row>
      </div>
    )
  }
}

export default ParametersDisplay