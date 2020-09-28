import "../css/style.css";
import axios from "axios";

let TICKERS = [];
const tickersURL = "http://localhost:8000/data/tickers/";

const updatedSection = document.getElementsByClassName("updated")[0];
const tickersSection = document.getElementsByClassName("tickers-list")[0];

window.addEventListener("load", async (e) => {
  const tickers = await axios.get(tickersURL);

  console.log(tickers.data.tickers.length);
  TICKERS = tickers.data.tickers;
  const tickersHTML = `
  <span>업데이트된 데이터 수: ${TICKERS.length}<span>
  `;

  updatedSection.innerHTML = tickersHTML;

  const searchInput = document.getElementById("search-input");

  searchInput.addEventListener("input", (e) => {
    if (searchInput.value == "") {
      tickersSection.innerHTML = "";
    } else {
      let filteredTickers = TICKERS.filter((ticker) =>
        ticker.includes(searchInput.value.toUpperCase())
      ).splice(0, 10);
      let resultHTML = "";
      filteredTickers.forEach((ticker) => {
        resultHTML = resultHTML + `<div class="ticker">${ticker}</div>`;
      });
      tickersSection.innerHTML = resultHTML;
    }
  });
});
