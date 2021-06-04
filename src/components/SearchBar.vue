<template>
  <div>
    <div class="search-input">
      <!-- $event是实参，表示event对象 -->
      <!--
          输入搜索内容即时搜索，所以有一个keyup事件。
          按回车键有一个进入搜索内容页面，所以有一个keydown.enter事件
          按上下键可以选择列表条目
      -->
      <input ref="searchInput"
             class="inputInfo"
             type="text"
             placeholder="🔍 Search pictures"
             v-model="keyword"
             @keyup="get($event)"
             @keydown.enter="search()"
             @keydown.down="selectDown()"
             @keydown.up.prevent="selectUp()" @focus="ifFocus = true; " @blur="setFocusFalse()">
      <!-- 这是一个小叉叉，点击它可清除输入框内容 -->
      <span class="search-reset" @click="clearInput()">&times;</span>
      <button class="search-btn" @click="search()">Search</button>
      <div class="search-select">
        <!-- transition-group也是vue2.0中的新特性,tag='ul'表示用ul包裹v-for出来的li -->
        <transition-group name="itemfade" tag="ul" mode="out-in" v-cloak>
          <li v-show="ifFocus" v-for="(value,index) in listItem" :class="{selectback:index==now}"
              class="search-select-option search-select-list" @mouseover="selectHover(index); "
              @click="selectClick(index); " :key="value">
            {{ value }}
          </li>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script type="text/javascript">

export default {
  name: "SearchBar",
  props: {
    listItem: {// history search keywords or inspirations
      type: Array,
      default: () => []
    }
  },
  data: function () {
    return {
      keyword: '',
      now: -1,
      searchIndex: 0,
      ifFocus: false,
    }
  },
  watch: {},
  methods: {
    // &event是实参，表示event对象
    get: function (ev) {

      if (ev.keyCode == 38 || ev.keyCode == 40) {
        return;
      }

      this.inspire();
    },
    selectDown: function () {
      this.now++;
      // 到达最后一个时，再按下就回到第一个
      if (this.now == this.listItem.length) {
        this.now = 0;
      }
      this.keyword = this.listItem[this.now];
    },
    selectUp: function () {
      this.now--;
      // 同上
      if (this.now == -1) {
        this.now = this.listItem.length - 1;
      }
      this.keyword = this.listItem[this.now];
    },
    selectHover: function (index) {
      this.now = index
    },
    selectClick: function (index) {
      this.keyword = this.listItem[index];
      this.search();
    },
    clearInput: function () {
      this.keyword = '';
    },
    setFocusFalse: function () {
      let that = this;
      setTimeout(function () {
        that.ifFocus = false;
      }, 300);
    },
    search: function () {
      this.$refs.searchInput.blur();
      this.ifFocus = false;

      this.$emit("search",
          {
            keyword: this.keyword,
          });

    },
    inspire: function () {

      this.$emit("inspire",
          {
            keyword: this.keyword,
          });
    }
  },
}
</script>

<style type="text/css">
.search-input {
  height: 45px;
  width: 600px;
  margin: 0 auto;
  margin-top: 10px;
  position: relative;
}

.search-input input {
  border: 1px solid #e4e4e4;
  background: #eeeeee;
  box-sizing: border-box;
  width: 500px;
  height: 45px;
  border-radius: 10px;
  font-size: 18px;
  float: left;
  padding-left: 10px;
  padding-right: 10px;
  overflow: hidden;
}

.search-btn {
  height: 45px;
  width: 100px;
  border: 2px darkblue;
  border-radius: 10px;
  background-color: darkcyan;
  color: white;
  font-size: 16px;
  font-weight: bold;
  float: left;
}

.search-btn {
  cursor: pointer
}

.search-select {
  position: absolute;
  top: 45px;
  width: 500px;
  border-radius: 10px;
  box-sizing: border-box;
  z-index: 999;
}

.search-select li {
  border: 1px solid #d4d4d4;;
  border-top: none;
  border-bottom: none;
  background-color: #fff;
  width: 100%
}

.search-select-option {
  box-sizing: border-box;
  padding: 7px 10px;
}

.selectback {
  background-color: #eee !important;
  cursor: pointer
}

input::-ms-clear {
  display: none
}

.search-reset {
  width: 21px;
  height: 21px;
  position: absolute;
  display: block;
  line-height: 21px;
  text-align: center;
  cursor: pointer;
  font-size: 20px;
  right: 110px;
  top: 12px
}

.search-select-list {
  transition: all 0.5s
}

.itemfade-enter,
.itemfade-leave-active {
  opacity: 0;
}

.itemfade-leave-active {
  position: absolute;
}

.selectback {
  background-color: #eee !important;
  cursor: pointer
}

.search-select ul {
  margin: 0;
  text-align: left;
}
</style>
