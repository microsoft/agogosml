const express = require('express')
const https = require('http');
const app = express()
const port = 3001

app.get('/', (req, res) => {
    console.log('Output adapter!')
    res.send('Output adapter!')
})

var server = app.listen(port, () => console.log(`Output adapter app listening on port ${port}!`))

app.get('/shutdown', (req, res) => {
    console.log('Output adapter is shutting down')
    res.send('Output adapter is shutting down')
    server.close()
    process.exit()
})

function shutDownInput(arg) {
    console.log('calling shutdown for input apps');
    https.get('http://input-adapter.agogosml.com:' + arg + '/shutdown')
  }
  
setTimeout(shutDownInput, 5000, 3000);
  