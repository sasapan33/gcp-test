require('dotenv').config()
var express = require('express');
const app = express()
const conn = require('./cloudsql');

//新增資料到db
app.route('/insert').get(function(req, res, next) {
  console.log('insert---', req.query)
  console.log('===')
  //insert
  const str_insert = 'insert into entries (guestName,content) values (?,?)'
  //insert data從query string拿
  const params = [req.query.guestName?req.query.guestName:null, req.query.content?req.query.content:null]
  conn.query(str_insert, params, function(err, result){
    if (err) throw err;
    console.log("1 record inserted");
  })
  //insert完後redirect
  res.redirect('/query')
});

//query table
app.route('/query').get(function(req, res, next) {
  conn.query(
      "SELECT * FROM `entries`",
      function(error, results, fields) {
        if (error) throw error;
        res.json(results);
      }
    );
  });

app.get('/', (req, res) => {
  setTimeout(() => {
    console.log('AAA')
    res.send('Hello World')
  }, 300)
})

app.listen(3000)
