<template>
  <v-app id="mainpage"
         class="backgroundImage"
         :style="backgroundimage">
    <v-main>
      <v-container>
        <SearchBar
            v-bind:my-data="historySearch"
            v-on:search="search"/>

      </v-container>
    </v-main>
    <v-spacer></v-spacer>
    <v-footer
        style=" filter:alpha(opacity:30); opacity:0.7; clear: both;display: block;text-align: center;margin: 0px auto;position: absolute;bottom: 0%;width: 100%;">
      ©2021, Tsinghua
    </v-footer>
  </v-app>
</template>

<script>
import SearchBar from "@/components/SearchBar";


export default {
  name: "MainPage",
  components: {SearchBar},
  data() {
    return {
      historySearch: ["123", "456", "789"],// 历史搜索关键词信息
      result: [],// 搜索结果信息；格式为[title,url]
      backgroundimage: "url(https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fdpic.tiankong.com%2Fs1%2F2h%2FQJ8879664576.jpg&refer=http%3A%2F%2Fdpic.tiankong.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625233227&t=c4e40368a5e3a774032107f60a13c07c)"
    }
  },
  methods: {
    search: function (msg) {
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

      // get hits, which is a Json
      this.$http.get("api/_search?q=descriptions:" + keyword).then((res) => {
        let hits = res.data.hits.hits;
        console.log(hits);
        for (let i = 0; i < hits.length; i++) {
          let source = hits[i]["_source"];
          let title = source["verbose-info"]["title"];
          let url = source["url"];
          this.result.push([title, url]);
        }
        console.log(this.result);
      }, (err) => {
        let error = err.json();
        console.log(error);
      })
    },
  }
}
</script>

<style scoped>

</style>
