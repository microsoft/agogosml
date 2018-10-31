const express = require('express')
var rp = require('request-promise');
const app = express()
const port = 3000

app.get('/', (req, res) => {
    res.send('Input adapter!')
})

var server = app.listen(port, () => console.log(`Input adapter app listening on port ${port}!`))

app.get('/shutdown', (req, res) => {
    console.log('Input adapter is shutting down')
    console.log('Triggering output adapter shut down as well')
    rp('http://output-adapter.agogosml.com:3001/shutdown').then(()=> {
      server.close()
      process.exit()
    })
})