# searchengine

## Backend setup
Read `scripts/readme.md` for details.

## Frontend setup && Run the app
```
npm install
npm run serve
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).



## elastic API

- get server status

  ```javascript
  GET-url:"ip:port/_cat/health?v"
  // code example:
  this.$http.get("api/_cat/health?v").then((res) => {
  	console.log(res);
  }, (err) => {
  	console.log(err);
  });
  ```

- search

  ```
  
  ```

- etc.

