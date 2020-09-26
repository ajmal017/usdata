const express = require("express");
const path = require("path");
var cors = require("cors");

const PORT = 8888;
const HOST = "0.0.0.0";

const app = express(); // 앱 시작
app.set("views", `${__dirname}/dist`); // HTML 파일 연결
app.set("view engine", "ejs");
app.engine("html", require("ejs").renderFile);

app.use(cors());
app.use(express.static(`${__dirname}/dist`)); // CSS 파일 연결

app.listen(PORT, HOST);
console.log(`서버가 http://${HOST}:${PORT} 에서 작동하고 있습니다.`);

app.get("/", (req, res) => {
  res.render("index.html");
});
