import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import openSocket from 'socket.io-client'
import ReactSpeedometer from 'react-d3-speedometer'

const websocketServer = 'fit5.fit-uet.tk:9001'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      'Temperature': 0
    }
    const socket = openSocket(websocketServer)
    socket.on('send data', (json) => {
      console.log(json)
      this.setState({
        'Temperature': parseInt(json.message, 10)
      })
    })
  }
  
  render() {
    return (
      <div className="App">
        <ReactSpeedometer value={this.state.Temperature} minValue={-50} maxValue={50} startColor="#ff471a" endColor="#ff471a"/>
      </div>
    );
  }
}

export default App;
