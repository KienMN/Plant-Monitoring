import React, { Component } from 'react'
import { LineChart } from 'react-d3-components'
import openSocket from 'socket.io-client'

const websocketServer = 'localhost:9001'

export default class Demo extends Component {
  constructor(props) {
    super(props)
    this.state = {
      'socket': openSocket(websocketServer),
      'demoData': [{
        label: '',
        values: [{ x: 0, y: 0 }]
      }],
      'width': 700,
      'height': 400
    }
    this.state.socket.on('webapp demo data', (json) => {
      console.log(json)
      this.setState({
        'demoData': json.demoData
      })
    })
    this.state.socket.emit('get demo data')
  }

  render() {
    return (
      <div>
        <h3>Pumping time prediction demo</h3>
        <LineChart data={this.state.demoData}
          width={this.state.width}
          height={this.state.height}
          margin={{ top: 10, bottom: 50, left: 50, right: 10 }}
          xAxis={{ label: "Time steps" }}
          yAxis={{ label: "Soil moisture" }}
        />
      </div>
    )
  }
}