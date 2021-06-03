<template>
  <div>
    <v-app id="mainpage"
           class="backgroundImage"
           :style="backgroundimage">
      <v-main>
        <v-container>
          <SearchBar
              v-bind:my-data="historySearch"
              v-on:search="inspire"/>
              <!-- v-on:search="search"/> -->
          <p></p>
          <PictureBook
              v-bind:my-info="result"/>
        </v-container>
      </v-main>
      <v-spacer></v-spacer>
      <v-footer
          style=" filter:alpha(opacity:30); opacity:0.7; clear: both;display: block;text-align: center;margin: 0px auto;position: absolute;bottom: 0%;width: 100%;">
        ©2021, Tsinghua
      </v-footer>
    </v-app>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import PictureBook from "@/components/PictureBook";

export default {
  name: "MainPage",
  components: {PictureBook, SearchBar},
  data() {
    return {
      historySearch: ["lake", "mountain", "air"],// 历史搜索关键词信息
      result: [],// 搜索结果信息；格式为[title,url]
      inspire_lines: [],// 提示信息
      backgroundimage: "url(https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdpic.tiankong.com%2Fs1%2F2h%2FQJ8879664576.jpg&refer=http%3A%2F%2Fdpic.tiankong.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625233227&t=c4e40368a5e3a774032107f60a13c07c)"
    }
  },
  methods: {
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
      // TODO:发送搜索请求，填进result
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
      this.$http.post("api/_search?size=20", config).then((res)=>{
        let hits = res.data.hits.hits;

        for (let i = 0; i < hits.length; i++) {
          let source = hits[i]["_source"];
          let title = source["verbose-info"]["title"];
          let url = source["url"];
          this.result.push({
            "title": title,
            "url": url,
          });
        }
        console.log(this.result);
      }, (err) => {
        let error = err.json();
        console.log(error);
      })
    },
    inspire: function (keyword) {
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
      this.$http.post("api/_search?size=20", config).then((res)=>{
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
              let nextchar = lines[i2][pos+keyword.length];
              if ((nextchar >= "A" && nextchar <= "Z") || (nextchar >= "a" && nextchar <= "z")) {
                good_fit.push(lines[i2]);
              }
              else {
                best_fit.push(lines[i2]);
              }
            }
            else {
              norm_fit.push(lines[i2]);
            }
          }
        }
        this.inspire_lines.push(...best_fit)
        this.inspire_lines.push(...good_fit)
        this.inspire_lines.push(...norm_fit)
        console.log(this.inspire_lines)
      }, (err) => {
        let error = err.json();
        console.log(error);
      });
    },
  }
}
</script>

<style scoped>

</style>
