import React, { Component } from 'react';
import openSocket from 'socket.io-client'
import ReactSpeedometer from 'react-d3-speedometer'
import { Button, Row, Col } from 'react-bootstrap'

const websocketServer = 'localhost:9001'

class ParametersDisplay extends Component {
  constructor(props) {
    super(props)
    this.state = {
      'Temperature': 0,
      'Humidity': 0,
      'SoilMoisture': 0,
      'LightIntensity': 0
    }
    let socket = openSocket(websocketServer)
    socket.on('send data', (json) => {
      console.log(json)
      switch (json.topic) {
        case "AT2018/Temperature":
          this.setState({
            'Temperature': parseInt(json.message, 10)
          })
          break
        case "AT2018/Humidity":
          this.setState({
            'Humidity': parseInt(json.message, 10)
          })
          break
        case "AT2018/SoilMoisture":
          let soilMoisture = parseInt(json.message, 10)
          soilMoisture = (1024 - soilMoisture) * 100 / 1024
          this.setState({
            'SoilMoisture': soilMoisture
          })
          break
        default:
          break
      }
    })
  }

  render() {
    return (
      <div>
        <Row>
          <Col md={3} sm={6} xs={12}>
            <p>Temperature</p>
            <ReactSpeedometer value={this.state.Temperature} minValue={-50} maxValue={50} startColor="#ff471a" endColor="#ff471a" />
          </Col>
          <Col md={3} sm={6} xs={12}>
            <p>Humidity</p>
            <ReactSpeedometer value={this.state.Humidity} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" />
          </Col>
          <Col md={3} sm={6} xs={12}>
            <p>Soil moisture</p>
            <ReactSpeedometer value={this.state.SoilMoisture} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" />
          </Col>
          <Col md={3} sm={6} xs={12}>
            <p>Light intensity</p>
            <ReactSpeedometer value={this.state.LightIntensity} minValue={0} maxValue={100} startColor="#ff471a" endColor="#ff471a" />
          </Col>
        </Row>
        
        
        <Button bsStyle="primary">Click me</Button>
      </div>
    )
  }
}

export default ParametersDisplay