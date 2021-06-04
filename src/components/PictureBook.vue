<template>
  <div>
    <div class="picture-book">
      <div>
        <stack :column-min-width="320" gutter-width="4" monitor-images-loaded="true">
          <stack-item v-for="(item, i) in myInfo" :key="i">
            <div class="imageDiv">
              <img class="image" height="260" width="320" :src="item.url" @click="jumpToSource(item.url)">
              <h4>{{ item.title }}</h4>
            </div>
          </stack-item>
        </stack>
      </div>
    </div>
  </div>
</template>

<script>
import {Stack, StackItem} from 'vue-stack-grid';

export default {
  name: "PictureBook",
  components: {Stack, StackItem},
  props: {
    myInfo: {// picture title & url
      type: Array,
      default: () => []
    }
  },
  data: function () {
    return {}
  },
  methods: {
    jumpToSource: function (url) {
      window.open(url);
    }
  }
}
</script>

<style type="text/css">
.imageDiv {
  background:#eeeeee;
  color:#2c3e50;
  border-radius: 10px;
  border: solid 1px #dddddd;
  padding: 10px;
  margin:10px 10px 10px 10px;
}

.image {
  border-radius: 10px;
}
</style>
