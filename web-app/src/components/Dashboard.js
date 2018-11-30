import React, { Component } from 'react';
import ParameterDisplay from './ParametersDisplay'
import WateringControl from './WateringControl';
import openSocket from 'socket.io-client'
import { Row, Col } from 'react-bootstrap';
import PumpingPrediction from './PumpingPrediction';
import Demo from './Demo';

const websocketServer = 'fit5.fit-uet.tk:9001'
// const websocketServer = 'localhost:9001'

export default class Dashboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      'Temperature': 0,
      'Humidity': 0,
      'SoilMoisture': 0,
      'LightIntensity': 0,
      'PumpingStatus': false,
      'socket': openSocket(websocketServer),
      'PumpingSpeed': 250,
      'predictedTime': null,
      'predictedDuration': null,
      'demoData': null
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

    this.state.socket.on('webapp prediction', (json) => {
      console.log(json)
      this.setState({
        'predictedTime': json.pumpingTime,
        'predictedDuration': json.duration
      })
    })

    this.state.socket.emit('get prediction from database')

    this.pumpRequest = this.pumpRequest.bind(this)
    this.changePumpingSpeed = this.changePumpingSpeed.bind(this)
  }

  pumpRequest() {
    let v = (this.state.PumpingStatus) ? 0 : this.state.PumpingSpeed
    this.state.socket.emit("pumping", { value: v })
  }

  changePumpingSpeed(e) {
    let newSpeed = parseInt(e.target.value, 10)
    this.setState({
      "PumpingSpeed": newSpeed
    })
    if (this.state.pumpingStatus) {
      console.log(newSpeed)
      this.state.socket.emit("pumping", { value: newSpeed })
    }
  }

  render() {
    return (
      <div>
        <ParameterDisplay temperature={this.state.Temperature} humidity={this.state.Humidity}
          soilMoisture={this.state.SoilMoisture} lightIntensity={this.state.LightIntensity} />
        <Row>
          <Col sm={6} xs={12}>
            {/* <h3>Average last 24 hours</h3> */}
            <Demo demoData={this.state.demoData}/>
            {/* <PumpingPrediction predictedTime={this.state.predictedTime} predictedDuration={this.state.predictedDuration}/> */}
          </Col>
          <Col sm={6} xs={12}>
            <WateringControl pumpingStatus={this.state.PumpingStatus} pump={this.pumpRequest} speed={this.state.PumpingSpeed} changeSpeed={this.changePumpingSpeed} />
          </Col>
        </Row>
        
      </div >
    )
  }
}