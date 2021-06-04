<template>
  <div>
    <v-app id="mainpage"
           class="backgroundImage">
      <h1 class=" title " @click="clearAll()">Simple Picture Search</h1>
      <v-main>
        <v-container>
          <SearchBar
              ref="searchBar"
              v-bind:list-item="listItem"
              v-on:search="search"
              v-on:inspire="inspire"/>
          <p></p>
          <PictureBook
              v-bind:my-info="result"/>
        </v-container>
      </v-main>
      <v-spacer></v-spacer>
    </v-app>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import PictureBook from "@/components/PictureBook";

function rgb2hsv(rgb) {
  let r = rgb[0];
  let g = rgb[1];
  let b = rgb[2];
  let rabs, gabs, babs, rr, gg, bb, h, s, v, diff, diffc, percentRoundFn;
  rabs = r / 255;
  gabs = g / 255;
  babs = b / 255;
  v = Math.max(rabs, gabs, babs),
      diff = v - Math.min(rabs, gabs, babs);
  diffc = c => (v - c) / 6 / diff + 1 / 2;
  percentRoundFn = num => Math.round(num * 100) / 100;
  if (diff == 0) {
    h = s = 0;
  } else {
    s = diff / v;
    rr = diffc(rabs);
    gg = diffc(gabs);
    bb = diffc(babs);

    if (rabs === v) {
      h = bb - gg;
    } else if (gabs === v) {
      h = (1 / 3) + rr - bb;
    } else if (babs === v) {
      h = (2 / 3) + gg - rr;
    }
    if (h < 0) {
      h += 1;
    } else if (h > 1) {
      h -= 1;
    }
  }
  return {
    h: Math.round(h * 360),
    s: percentRoundFn(s * 100),
    v: percentRoundFn(v * 100)
  };
}

let hsvRange = {
  "black": [[0, 360], [0, 100], [0, 17]],
  "gray": [[0, 360], [0, 17], [17, 86]],
  "white": [[0, 360], [0, 17], [86, 100]],
  "red": [[0, 40, 320, 360], [17, 100], [18, 100]],
  "green": [[80, 160], [17, 100], [18, 100]],
  "blue": [[200, 280], [17, 100], [18, 100]],
}

export default {
  name: "MainPage",
  components: {PictureBook, SearchBar},
  created() {
    this.listItem = this.historySearch;
  },
  data() {
    return {
      historySearch: ["lake", "mountain", "air", "dog"],// 历史搜索关键词信息
      result: [],// 搜索结果信息；格式为[title,url]
      inspire_lines: [],// 提示信息
      listItem: [],
    }
  },
  methods: {
    clearAll: function () {
      this.$refs.searchBar.keyword = "";
      this.result = [];
    },
    search: function (msg) {
      this.result = [];

      let keyword = msg.keyword;
      let include = this.historySearch.indexOf(keyword);
      if (include !== -1) {
        let special = this.historySearch[include];
        this.historySearch.splice(include, 1);
        this.historySearch.unshift(special);
      } else {
        if (this.historySearch.length < 8) {
          this.historySearch.unshift(keyword);
        } else {
          this.historySearch.pop();
          this.historySearch.unshift(keyword);
        }
      }

      // get advanced keyword
      let keywords = keyword.split(/[ ]+/);
      keyword = keywords[0];
      // extract discriptions
      let colorSpecified = false;
      let sizeSpecified = false;
      if (keywords.length > 1) {
        for (let i = 1; i < keywords.length; ++i) {
          let description = keywords[i].split(/[:]+/);
          if (description[0] === "color" || description[0] === "colour") {
            colorSpecified = description[1];
          } else if (description[0] === "size") {
            sizeSpecified = description[1];
          }
        }
      }

      let config = {
        "query": {
          "match": {
            "descriptions": {
              "query": keyword,
              "fuzziness": "AUTO"
            }
          }
        }
      }
      this.$http.post("api/_search?size=20", config).then((res) => {

        let hits = res.data.hits.hits;
        console.log(hits);

        for (let i = 0; i < hits.length; i++) {
          let source = hits[i]["_source"];
          let title = source["verbose-info"]["title"];
          let url = source["url"];
          let accept = true;

          // normal case
          if ((!colorSpecified) && (!sizeSpecified)) {
            this.result.push({
              "title": title,
              "url": url,
            });
            continue;
          }

          // advanced search result
          if (sizeSpecified) {
            let size = source["verbose-info"]["original-size"];

            if (sizeSpecified === "small") {
              if (size > 400000) {
                accept = false;
              }
            } else if (sizeSpecified === "medium") {
              if (size <= 400000 || size > 3000000) {
                accept = false;
              }
            } else if (sizeSpecified === "large" || sizeSpecified === "big") {
              if (size <= 3000000) {
                accept = false;
              }
            }
          }

          if (!colorSpecified) {
            if (accept) {
              this.result.push({
                "title": title,
                "url": url,
              });
            }
            continue;
          }

          // sync till onload function finished!
          let promise = new Promise(function (resolve) {

            console.log(colorSpecified);
            let img_url = url + "?" + Date.parse(new Date());

            let img = new Image();
            img.src = img_url;
            img.crossOrigin = "Anonymous";
            img.onload = function () {
              let width = img.width;
              let height = img.height;

              let canvas = document.createElement('canvas');
              canvas.width = width;
              canvas.height = height;

              let ctx = canvas.getContext('2d');
              ctx.drawImage(img, 0, 0);

              let data = ctx.getImageData(0, 0, width, height);
              // 变换为一维数据RGBA
              data = data.data;
              let imgArr = [];
              let pace = Math.round(Math.sqrt(data.length));
              for (let i = 0; i < data.length; i += 4 * pace) {
                imgArr.push([data[i], data[i + 1], data[i + 2]])
              }
              // 阻塞版本
              var kMeans = require('kmeans-js');

              let clusterNum = 8;

              var km = new kMeans({
                K: clusterNum
              });

              km.cluster(imgArr);
              while (km.step()) {
                km.findClosestCentroids();
                km.moveCentroids();
                if (km.hasConverged()) break;
              }

              let total_cnum = 0;
              let rate = 1;   // 限制比率，1表示只判断像素数目超过平均值的颜色，rate越小则判断范围越大
              for (let t = 0; t < clusterNum; ++t) {
                total_cnum += km.clusters[t].length;
              }
              let hsv_range = hsvRange[colorSpecified];
              let gflag = false;
              for (let t = 0; t < clusterNum; ++t) {
                if (km.clusters[t].length < total_cnum * rate / clusterNum)
                  continue;
                let color = rgb2hsv(km.centroids[t]);
                color = [color.h, color.s, color.v];
                let flag = true;
                for (let t = 0; t < 3; ++t) {
                  if (hsv_range[t].length == 2 && (color[t] < hsv_range[t][0] || color[t] > hsv_range[t][1])) {
                    flag = false;
                    break;
                  }
                  if (hsv_range[t].length == 4 && ((color[t] < hsv_range[t][0] || color[t] > hsv_range[t][1]) && (color[t] < hsv_range[t][2] || color[t] > hsv_range[t][3]))) {
                    flag = false;
                    break;
                  }
                }
                if (flag) {
                  gflag = true;
                  break;
                }
              }
              if (!gflag) {
                accept = false;
              }
              resolve();
            };
          });

          promise.then(() => {
            if (accept) {
              this.result.push({
                "title": title,
                "url": url,
              });
            }
          });
        }
        console.log(this.result);
      }, (err) => {
        let error = err.json();
        console.log(error);
      })
    },
    inspire: function (keyword) {
      if (keyword.keyword === "") {
        this.listItem = this.historySearch;
        return;
      }
      keyword = keyword.keyword;
      let lines = new Set();
      this.inspire_lines = [];
      let config = {
        "query": {
          "match": {
            "descriptions": {
              "query": keyword,
              "fuzziness": 15 // TODO: 调参，大了模糊（吧），似乎修改字符数不超过2个[https://www.elastic.co/guide/en/elasticsearch/reference/7.13/query-dsl-fuzzy-query.html]
            }
          }
        }
      }
      let best_fit = [];
      let good_fit = [];
      let norm_fit = [];
      this.$http.post("api/_search?size=20", config).then((res) => {
        let hits = res.data.hits.hits;
        for (var i = 0; i < hits.length; ++i) {
          for (var j = 0; j < hits[i]._source.descriptions.length; ++j) {
            let line = hits[i]._source.descriptions[j];
            lines.add(line);
          }
        }
        lines = Array.from(lines);
        for (var i2 = 0; i2 < lines.length; ++i2) {
          let pos = lines[i2].toLocaleLowerCase().indexOf(keyword.toLocaleLowerCase());
          if (pos >= 0) {
            if (pos == 0) {
              let nextchar = lines[i2][pos + keyword.length];
              if ((nextchar >= "A" && nextchar <= "Z") || (nextchar >= "a" && nextchar <= "z")) {
                good_fit.push(lines[i2]);
              } else {
                best_fit.push(lines[i2]);
              }
            } else {
              norm_fit.push(lines[i2]);
            }
          }
        }
        this.inspire_lines.push(...best_fit);
        this.inspire_lines.push(...good_fit);
        this.inspire_lines.push(...norm_fit);
        this.inspire_lines = this.inspire_lines.slice(0, 8);
        console.log(this.inspire_lines);
        this.listItem = this.inspire_lines;
      }, (err) => {
        let error = err.json();
        console.log(error);
      });
    },
  }
}
</script>

<style type="text/css">
.title {
  color: mediumaquamarine;
}

.footer {
  filter: alpha(opacity:30);
  opacity: 0.7;
  clear: both;
  display: block;
  text-align: center;
  margin: 0px auto;
  position: absolute;
  bottom: 0%;
  width: 100%;
}

</style>
