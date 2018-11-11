import React, { Component } from 'react';
import ParameterDisplay from './ParametersDisplay'
import WateringControl from './WateringControl';
import openSocket from 'socket.io-client'
import { Row, Col } from 'react-bootstrap';

const websocketServer = 'fit5.fit-uet.tk:9001'

export default class Dashboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      'Temperature': 0,
      'Humidity': 0,
      'SoilMoisture': 0,
      'LightIntensity': 0,
      'PumpingStatus': false,
      'socket': openSocket(websocketServer)
    }
    this.state.socket.on('webapp monitoring', (json) => {
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
          this.setState({
            'SoilMoisture': parseInt(json.message, 10)
          })
          break
        case "AT2018/LightIntensity":
          let lightIntensity = parseInt(json.message, 10)
          this.setState({
            'LightIntensity': lightIntensity
          })
          break
        case "AT2018/PumpingStatus":
          let pumpingStatus = (parseInt(json.message, 10) !== 0)
          this.setState({
            'PumpingStatus': pumpingStatus
          })
          break
        default:
          break
      }
    })

    this.pumpRequest = this.pumpRequest.bind(this)
  }

  pumpRequest() {
    let v = (this.state.PumpingStatus) ? 0 : 512
    this.state.socket.emit("pumping", { value: v })
  }

  render() {
    return (
      <div>
        <ParameterDisplay temperature={this.state.Temperature} humidity={this.state.Humidity}
          soilMoisture={this.state.SoilMoisture} lightIntensity={this.state.LightIntensity} />
        <Row>
          <Col sm={6} xs={12}>
            <h3>Average last 24 hours</h3>
          </Col>
          <Col sm={6} xs={12}>
            <WateringControl pumpingStatus={this.state.PumpingStatus} pump={this.pumpRequest} />
          </Col>
        </Row>

      </div>
    )
  }
}